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

# CORS configuration - MUST BE FIRST
origins = [
    "https://crmpxx-crm-frontend.80opze.easypanel.host",
    "https://crm.projectexinoxano.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# EXCEPTION HANDLER (DEBUG)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    tb_str = traceback.format_exc()
    logger.error(f"GLOBAL ERROR: {tb_str}")
    
    # Retornem 200 temporalment per saltar-nos el bloqueig de CORS del navegador i llegir l'error
    # Només per a DEBUG de producció
    # Determinar origen de forma segura per al CORS d'errors
    origin = request.headers.get("origin")
    if not origin or origin == "null":
        origin = "*"
    
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
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
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
from routers import municipis_api
app.include_router(municipis_api.router, prefix="/api/v2/municipis")
app.include_router(municipis_v2.router)
app.include_router(emails_v2.router, prefix="/api/v2")
app.include_router(activitats_v2.router, prefix="/api/v2")
app.include_router(auth.router)
app.include_router(usuaris.router)
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
async def repair_db_endpoint(db: Session = Depends(get_db)):
    """Endpoint de diagnòstic i reparació profunda."""
    from models_v2 import MunicipiLifecycle
    from sqlalchemy import text
    try:
        # A. DIAGNÒSTIC: Quins valors té l'Enum ara? (busquem en tot l'esquema)
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT n.nspname as schema, t.typname as type, e.enumlabel as value
                FROM pg_type t 
                JOIN pg_enum e ON t.oid = e.enumtypid  
                JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
                WHERE t.typname = 'etapa_funnel'
            """))
            details = [{"schema": r[0], "type": r[1], "value": r[2]} for r in result]
            existing_values = [d["value"] for d in details]
        
        # B. REPARACIÓ ENUM (amb l'esquema public per si de cas)
        if 'lead' not in existing_values:
            try:
                with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                    conn.execute(text("ALTER TYPE public.etapa_funnel ADD VALUE 'lead'"))
                existing_values.append('lead')
            except Exception as e:
                return {"status": "error", "at": "alter_type", "error": str(e), "existing": details}

        # C. SANEJAMENT AMB SQL RAW (per evitar problemes de casting de Pydantic/SQLAlchemy)
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            # Fix EtapaActual NULL -> lead (usant cast explícit)
            res1 = conn.execute(text("UPDATE municipis_lifecycle SET etapa_actual = 'lead'::public.etapa_funnel WHERE etapa_actual IS NULL"))
            # Fix Temperatura NULL -> freda
            res2 = conn.execute(text("UPDATE municipis_lifecycle SET temperatura = 'freda'::public.temperatura WHERE temperatura IS NULL"))
        
        return {
            "status": "success", 
            "db_details": details,
            "message": "Sanejament realitzat amb SQL Directe."
        }
    except Exception as e:
        logger.error(f"Error a /repair-db: {e}")
        return {"status": "error", "message": str(e), "db_details": details if 'details' in locals() else []}

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
    import os
    return {"keys": list(os.environ.keys())}

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
