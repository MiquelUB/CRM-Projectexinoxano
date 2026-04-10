import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Error clar per a producció
    logger.error("FATAL: DATABASE_URL no definida a l'entorn!")
    # No posem fallback per evitar connexions a hosts inexistents que causen 500s silenciosos
    # En local, el load_dotenv() hauria d'haver carregat el .env
    raise ValueError("Falta la configuració de DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-csearch_path=public"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        # We can't return a JSONResponse here easily as it is a generator
        # but we can at least log it or raise a more descriptive error if we had a logger
        raise e
