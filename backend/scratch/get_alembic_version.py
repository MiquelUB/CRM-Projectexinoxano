
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)
with engine.connect() as conn:
    res = conn.execute(text("SELECT version_num FROM alembic_version"))
    print(f"Versió actual d'Alembic: {res.scalar()}")
