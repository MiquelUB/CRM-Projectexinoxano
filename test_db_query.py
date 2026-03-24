import os
import sys
from dotenv import load_dotenv

# Add backend to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

load_dotenv("backend/.env")

from database import SessionLocal
import models

def test_query():
    db = SessionLocal()
    try:
        print("Querying Municipis...")
        municipis = db.query(models.Municipi).all()
        print(f"Success! Found {len(municipis)} municipis.")
    except Exception as e:
        import traceback
        print("Error encountered:")
        traceback.print_exc()

if __name__ == "__main__":
    test_query()
