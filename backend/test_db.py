import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Testing connection to {db_url}...")

try:
    engine = sqlalchemy.create_engine(db_url)
    with engine.connect() as conn:
        print("SUCCESS: Connected to database!")
except Exception as e:
    print(f"FAILED: {e}")
