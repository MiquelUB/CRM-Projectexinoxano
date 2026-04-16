
from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)
inspector = inspect(engine)

print("Taules a la base de dades:")
for table_name in inspector.get_table_names():
    print(f"- {table_name}")
