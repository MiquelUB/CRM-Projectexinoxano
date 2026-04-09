import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://pxx_admin:b86f95465942a859661e@crmpxx_db-crmpxx:5432/crm_pxx?sslmode=disable"
)

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
