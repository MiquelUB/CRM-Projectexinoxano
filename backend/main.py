import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal, get_db
import models
from auth import get_password_hash
from routers import municipis, contactes, deals, auth, emails, llicencies, pagaments, alertes, usuaris, agent, tasques, dashboard, municipis_v2, emails_v2, activitats_v2
import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start APScheduler jobs
    scheduler.start_scheduler()
    
    # Schema migrations handled exclusively by Alembic
    
    # Create default admin user if not exists
    try:
        if SessionLocal is not None:
            db = SessionLocal()
            try:
                admin_user = db.query(models.Usuari).filter(models.Usuari.email == "admin@projectexinoxano.cat").first()
                if not admin_user:
                    admin = models.Usuari(
                        email="admin@projectexinoxano.cat",
                        password_hash=get_password_hash("pxx_admin_2026!"),
                        nom="Admin PXX",
                        rol="admin"
                    )
                    db.add(admin)
                    db.commit()
            finally:
                db.close()
        else:
            print("AVÍS: SessionLocal no disponible en arrencar. Saltant verificació d'admin.")
    except Exception as e:
        print(f"Error en el procés de startup: {e}")
    
    yield
    
    # Stop APScheduler
    scheduler.shutdown_scheduler()

app = FastAPI(
    title="CRM PXX API",
    description="API for the Projecte Xino Xano CRM",
    version="1.0.0",
    lifespan=lifespan
)

import logging
logger = logging.getLogger("uvicorn.error")

# CORS configuration
origins = [
    "https://crmpxx-crm-front.80opze.easypanel.host",
    "https://crmpxx.projectexinoxano.cat",
    "http://localhost:3000",
    "http://localhost:3001"
]

# EXCEPTION HANDLER (DEBUG)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    tb_str = traceback.format_exc()
    logger.error(f"GLOBAL ERROR: {tb_str}")
    
    # Retornem 500 amb headers CORS explícits
    # Determinar origen de forma segura per al CORS d'errors
    origin = request.headers.get("origin") or "*"
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "traceback": tb_str,
            "path": request.url.path
        },
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.middleware("http")
async def monitor_v1_usage(request: Request, call_next):
    # Monitorització d'endpoints obsolets V1
    v1_paths = {
        "/municipis": "municipis",
        "/contactes": "contactes",
        "/deals": "deals",
        "/emails": "emails",
        "/tasques": "tasques"
    }
    
    path = request.url.path
    if path.startswith("/"):
        # Extreure el primer segment del path
        first_segment = "/" + path.split("/")[1] if len(path.split("/")) > 1 else path
        
        if first_segment in v1_paths:
            # Si és un endpoint V1 pur (sense v2 al path)
            if "_v2" not in path and "emails_v2" not in path and "api/v2" not in path:
                taula = v1_paths[first_segment]
                logger.warning(f"[DEPRECATED] Query a taula '{taula}' des de endpoint '{path}'")
    
    response = await call_next(request)
    return response

@app.middleware("http")
async def force_https_middleware(request: Request, call_next):
    if request.headers.get("x-forwarded-proto") == "https":
        request.scope["scheme"] = "https"
    response = await call_next(request)
    return response


# Include routers
app.include_router(dashboard.router)
@app.get("/")
async def root_health():
    return {"status": "online", "message": "CRM PXX Backend (V_BETA_4_CORS) is running", "timestamp": "2026-04-10T11:55"}

from routers import municipis_api
app.include_router(municipis_api.router, prefix="/api/v2/municipis")
app.include_router(emails_v2.router, prefix="/api/v2")
app.include_router(activitats_v2.router, prefix="/api/v2")
app.include_router(auth.router)
app.include_router(usuaris.router)
app.include_router(municipis_v2.router, prefix="/municipis_v2")
app.include_router(municipis_v2.router, prefix="/municipis_lifecycle")
app.include_router(contactes.router, prefix="/contactes", tags=["contactes"])
app.include_router(municipis.router)
app.include_router(contactes.router)
app.include_router(deals.router)
app.include_router(emails.router)
app.include_router(llicencies.router)
app.include_router(pagaments.router)
app.include_router(alertes.router)
app.include_router(agent.router)
app.include_router(agent.tracking_router)
app.include_router(tasques.router)

@app.get("/repair-db")
@app.get("/repair-db/")
async def repair_db_endpoint(db: Session = Depends(get_db)):
    """Endpoint de diagnòstic i reparació profunda de tots els Enums."""
    from models_v2 import MunicipiLifecycle
    from sqlalchemy import text
    try:
        # A. DIAGNÒSTIC: Quins valors tenen els Enums ara?
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT t.typname, e.enumlabel
                FROM pg_type t 
                JOIN pg_enum e ON t.oid = e.enumtypid  
                WHERE t.typname IN ('etapa_funnel', 'temperatura')
            """))
            rows = result.fetchall()
            enums = {}
            for row in rows:
                enums.setdefault(row[0], []).append(row[1])
        
        # B. REPARACIÓ ENUMS (fora de transacció)
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            # 1. Fix Funnel
            if 'lead' not in enums.get('etapa_funnel', []):
                try: conn.execute(text("ALTER TYPE public.etapa_funnel ADD VALUE 'lead'"))
                except: pass
            
            # 2. Fix Temperatura (Alineat amb models_v2.py: fred, templat, calent, bullent)
            for val in ['fred', 'templat', 'calent', 'bullent']:
                if val not in enums.get('temperatura', []):
                    try: conn.execute(text(f"ALTER TYPE public.temperatura ADD VALUE '{val}'"))
                    except: pass

        # D. REPARACIÓ D'ESTRUCTURA (Alineació final amb models_v2.py)
        results = []
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            # 1. Auditoria prèvia
            audit = conn.execute(text("""
                SELECT column_name, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'agent_memories_v2' 
                AND column_name IN ('municipi_id', 'usuari_id')
            """)).fetchall()
            results.append({"audit_before": {row[0]: row[1] for row in audit}})

            # 2. Afegir columnes de lifecycle si falten
            lifecycle_cols = {
                "valor_setup": "NUMERIC(10,2) DEFAULT 0",
                "valor_llicencia": "NUMERIC(10,2) DEFAULT 0",
                "proper_pas": "TEXT",
                "prioritat": "INTEGER DEFAULT 3",
                "data_seguiment": "TIMESTAMP WITH TIME ZONE",
                "notes_humanes": "TEXT"
            }
            for col, col_type in lifecycle_cols.items():
                try: 
                    conn.execute(text(f"ALTER TABLE municipis_lifecycle ADD COLUMN IF NOT EXISTS {col} {col_type}"))
                    results.append(f"Column {col} OK")
                except Exception as e: 
                    results.append(f"Column {col} Error: {str(e)}")

            # 3. Reparar activitats_municipi (created_at, updated_at)
            for col in ["created_at", "updated_at"]:
                try: 
                    conn.execute(text(f"ALTER TABLE activitats_municipi ADD COLUMN IF NOT EXISTS {col} TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"))
                    results.append(f"Column activitats_municipi.{col} OK")
                except Exception as e: 
                    results.append(f"Column activitats_municipi.{col} Error: {str(e)}")

            # 4. FIX AGRESSIU NOT NULL
            cols_to_relax = ["municipi_id", "usuari_id", "clau", "valor"]
            for col in cols_to_relax:
                try: 
                    conn.execute(text(f"ALTER TABLE agent_memories_v2 ALTER COLUMN {col} DROP NOT NULL"))
                    # Borrar possibles restriccions de check si n'hi haguessin
                    results.append(f"Drop NOT NULL {col} OK")
                except Exception as e: 
                    results.append(f"Drop NOT NULL {col} Error: {str(e)}")
            
            # 4. Auditoria posterior
            audit_post = conn.execute(text("""
                SELECT column_name, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'agent_memories_v2' 
                AND column_name IN ('municipi_id', 'usuari_id')
            """)).fetchall()
            results.append({"audit_after": {row[0]: row[1] for row in audit_post}})
        
        return {
            "status": "success", 
            "message": "Protocol de reparació i auditoria completat.",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error a /repair-db: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/db-check")
def db_check():
    from database import SessionLocal
    from sqlalchemy import text
    import traceback
    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            return {"status": "connected", "database": "ok"}
        except Exception as conn_e:
            return {
                "status": "error",
                "detail": str(conn_e),
                "traceback": traceback.format_exc()
            }
        finally:
            db.close()
    except Exception as e:
        return {
            "status": "session_init_error",
            "detail": str(e),
            "traceback": traceback.format_exc()
        }

@app.get("/env-check")
def env_check():
    """Endpoint per verificar si les variables d'entorn estan arribant al contenidor."""
    import os
    return {
        "DATABASE_URL": "Configurada" if os.getenv("DATABASE_URL") else "FALTA",
        "OPENROUTER_API_KEY": f"{os.getenv('OPENROUTER_API_KEY')[:6]}..." if os.getenv("OPENROUTER_API_KEY") else "FALTA",
        "DATABASE_URL_VAL": os.getenv("DATABASE_URL")[:20] + "..." if os.getenv("DATABASE_URL") else None
    }

@app.get("/dashboard/diari")
async def get_dashboard_diari(db: Session = Depends(get_db)):
    from services.prioritizer import get_daily_actions
    try:
        actions = await get_daily_actions(db)
        return actions
    except Exception as e:
        logger.error(f"Error a get_daily_actions: {e}")
        # Retornem una estructura buida però vàlida en comptes de petar
        return {
            "accions_prioritaries": [],
            "kpis": {"obertes": 0, "pendents": 0, "guanyades": 0},
            "error": "No s'han pogut carregar les accions de IA"
        }

@app.get("/inventory")
def get_inventory(db: Session = Depends(get_db)):
    from sqlalchemy import text
    results = {}
    try:
        # Version
        results["pg_version"] = db.execute(text("SELECT version()")).scalar()
        
        # V1 Tables
        v1_tables = ["municipis", "contactes", "deals", "emails"]
        results["v1"] = {}
        for table in v1_tables:
            try:
                results["v1"][table] = db.execute(text(f"SELECT count(*) FROM {table}")).scalar()
            except:
                results["v1"][table] = "Error/Missing"
        
        # V2 Tables
        v2_tables = ["municipis_lifecycle", "contactes_v2", "emails_v2", "tasques_v2", "activitats_municipi", "agent_memories_v2"]
        results["v2"] = {}
        for table in v2_tables:
            try:
                results["v2"][table] = db.execute(text(f"SELECT count(*) FROM {table}")).scalar()
            except:
                results["v2"][table] = "Error/Missing"
                
        return results
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Benvingut a l'API del CRM PXX - V2 DEBUG"}
