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
        db = SessionLocal()
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
        db.close()
    except Exception as e:
        print(f"Error during lifespan DB initialization: {e}")
    
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
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:3002",
    "http://127.0.0.1:3002",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://192.168.10.106:3000",
    "https://crm.projectexinoxano.cat",
    "https://api.projectexinoxano.cat",
    "https://crmpxx-crm-frontend.80opze.easypanel.host",
    "https://crmpxx-crm-frontend.80opze.easypanel.host/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
