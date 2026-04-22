
import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal, get_db
import models
from auth import get_password_hash
from routers import auth, alertes, usuaris, tasques, dashboard, municipis, emails, activitats, contactes, tracking
import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Run migrations/fixes (Contactes columns)
    try:
        from fix_contactes_db import fix_contactes_columns
        fix_contactes_columns()
    except Exception as e:
        print(f"Error migració contactes: {e}")

    # 2. Start APScheduler jobs (Email Sync)
    scheduler.start_scheduler()
    
    # 3. Create default admin user if not exists
    try:
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
                print("Usuari admin creat correctament.")
        except Exception as e:
            print(f"Error startup admin: {e}")
        finally:
            db.close()
    except Exception as e:
        print(f"Error lifespan startup: {e}")
    
    yield
    
    # Stop APScheduler
    scheduler.shutdown_scheduler()

app = FastAPI(
    title="CRM PXX Unified API",
    description="Unified backend for the CRM PXX project",
    version="2.0.0",
    lifespan=lifespan
)

import logging
logger = logging.getLogger("uvicorn.error")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.easypanel\.host|https://.*\.projectexinoxano\.cat|http://localhost:.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    tb_str = traceback.format_exc()
    logger.error(f"GLOBAL ERROR: {tb_str}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "traceback": tb_str if os.getenv("DEBUG") else None,
            "path": request.url.path
        }
    )

@app.middleware("http")
async def transparent_legacy_rewriter(request: Request, call_next):
    path = request.url.path
    
    # Traductor de rutes velles a noves (v1/v2/lifecycle -> unified)
    if "municipis_v2" in path or "_v2" in path or "municipis_lifecycle" in path:
        # 1. Cas especial: Llicència (v2 usava sub-ruta, vàrem passar a top-level amb query param)
        import re
        llicencia_match = re.match(r".*/municipis(?:_v2|_lifecycle)?/([^/]+)/llicencia.*", path)
        if llicencia_match:
            new_path = "/llicencies"
            new_query = f"deal_id={llicencia_match.group(1)}"
            request.scope["path"] = new_path
            request.scope["raw_path"] = new_path.encode()
            request.scope["query_string"] = new_query.encode()
            logger.info(f"🔄 [REWRITE SPECIAL] {path} -> {new_path}?{new_query}")
            return await call_next(request)

        # 2. Cas general
        new_path = path.replace("municipis_v2", "municipis") \
                       .replace("_v2", "") \
                       .replace("municipis_lifecycle", "municipis") \
                       .replace("//", "/")
        
        if "/municipis/contactes" in new_path:
            new_path = new_path.replace("/municipis/contactes", "/contactes")
        
        request.scope["path"] = new_path
        logger.info(f"🔄 [REWRITE] {path} -> {new_path}")

    if request.headers.get("x-forwarded-proto") == "https":
        request.scope["scheme"] = "https"
        
    response = await call_next(request)
    return response

@app.get("/debug/schema")
def debug_schema():
    from sqlalchemy import inspect
    try:
        inspector = inspect(engine)
        cols = inspector.get_columns("contactes")
        return {"table": "contactes", "columns": cols}
    except Exception as e:
        return {"error": str(e)}

# Standard health routes
@app.get("/")
async def root_health():
    return {
        "status": "online", 
        "message": "CRM PXX Unified Backend", 
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Include Unified Routers
app.include_router(auth.router)
app.include_router(usuaris.router)
app.include_router(dashboard.router)
app.include_router(municipis.router)
app.include_router(emails.router)
app.include_router(contactes.router)
app.include_router(activitats.router)
app.include_router(tasques.router)
app.include_router(alertes.router)
app.include_router(tracking.router)
