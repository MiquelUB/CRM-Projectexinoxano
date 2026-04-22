import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+pg8000://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+pg8000://", 1)
    
    # Netegem paràmetres com ?sslmode=require que pg8000 no suporta directament a la URL
    if "?" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.split("?")[0]

if not DATABASE_URL:
    logger.error("FATAL: DATABASE_URL no definida a l'entorn!")
    DATABASE_URL = "postgresql+pg8000://missing_url_error"

try:
    # Use pg8000 (pure python) to avoid C extension dependencies like libz.so.1
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Error creant l'engine de la BD: {e}")
    SessionLocal = None

Base = declarative_base()

def get_db():
    if SessionLocal is None:
        logger.error("Intent d'accés a BD sense SessionLocal inicialitzat")
        raise RuntimeError("La base de dades no està configurada correctament (SessionLocal is None)")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
