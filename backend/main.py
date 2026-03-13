from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import engine, Base, SessionLocal
import models
from auth import get_password_hash
from routers import municipis, contactes, deals, auth, emails, llicencies, pagaments, alertes, usuaris, agent, tasques
import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start APScheduler jobs
    scheduler.start_scheduler()
    
    # Schema migrations handled exclusively by Alembic
    
    # Create default admin user if not exists
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
    
    yield
    
    # Stop APScheduler
    scheduler.shutdown_scheduler()

app = FastAPI(
    title="CRM PXX API",
    description="API for the Projecte Xino Xano CRM",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:3002",
    "http://127.0.0.1:3002",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
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

@app.get("/")
def read_root():
    return {"message": "Benvingut a l'API del CRM PXX"}
