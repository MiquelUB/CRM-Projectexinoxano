import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# Load .env.local
if os.path.exists(".env.local"):
    load_dotenv(".env.local")
else:
    load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Connecting to: {db_url}")

try:
    engine = create_engine(db_url)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Connection successful!")
    print(f"Tables found ({len(tables)}): {tables}")
except Exception as e:
    print(f"Connection failed: {e}")
