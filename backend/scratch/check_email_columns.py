
from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)
inspector = inspect(engine)

print("Columnes de la taula 'emails':")
columns = inspector.get_columns('emails')
for c in columns:
    print(f"- {c['name']} ({c['type']})")
