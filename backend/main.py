
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
from routers import auth, alertes, usuaris, agent, tasques, dashboard, municipis, emails, activitats, contactes
import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start APScheduler jobs
    scheduler.start_scheduler()
    
    # Create default admin user if not exists
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
async def force_https_middleware(request: Request, call_next):
    if request.headers.get("x-forwarded-proto") == "https":
        request.scope["scheme"] = "https"
    response = await call_next(request)
    return response

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

# --- LEGACY ROUTE REDIRECTS (Compatibility Layer) ---
from fastapi.responses import RedirectResponse

@app.api_route("/municipis_v2/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def legacy_municipis_redirect(request: Request, path: str):
    url = f"/municipis/{path}" if path else "/municipis"
    query_params = str(request.query_params)
    if query_params: url += f"?{query_params}"
    return RedirectResponse(url=url, status_code=307)

@app.api_route("/contactes_v2/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def legacy_contactes_redirect(request: Request, path: str):
    url = f"/contactes/{path}" if path else "/contactes"
    query_params = str(request.query_params)
    if query_params: url += f"?{query_params}"
    return RedirectResponse(url=url, status_code=307)

@app.api_route("/emails_v2/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def legacy_emails_redirect(request: Request, path: str):
    url = f"/emails/{path}" if path else "/emails"
    query_params = str(request.query_params)
    if query_params: url += f"?{query_params}"
    return RedirectResponse(url=url, status_code=307)

@app.api_route("/municipis_lifecycle/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def legacy_lifecycle_redirect(request: Request, path: str):
    # Map lifecycle calls to the unified municipis router
    url = f"/municipis/{path}" if path else "/municipis"
    query_params = str(request.query_params)
    if query_params: url += f"?{query_params}"
    return RedirectResponse(url=url, status_code=307)
# ---------------------------------------------------

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
app.include_router(agent.router)
app.include_router(agent.tracking_router)
