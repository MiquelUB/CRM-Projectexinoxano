import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("FATAL: DATABASE_URL no definida a l'entorn!")
    # No llencem ValueError aquí per permetre que l'app arrenqui i ens doni logs pel navegador
    # Però l'engine fallarà quan s'intenti usar
    DATABASE_URL = "postgresql://missing_url_error"

try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"options": "-csearch_path=public"}
    )
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
