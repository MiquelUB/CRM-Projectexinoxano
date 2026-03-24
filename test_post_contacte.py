import os
import sys
from uuid import uuid4
from dotenv import load_dotenv

# Add backend to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

load_dotenv("backend/.env")

from database import SessionLocal
import models

def test_insert():
    db = SessionLocal()
    try:
        # First find a valid municipi to attach to
        municipi = db.query(models.Municipi).first()
        if not municipi:
            print("No municipi found to attach contact. Exiting.")
            return

        print(f"Using MunicipId: {municipi.id}")

        new_contacte = models.Contacte(
            municipi_id=municipi.id,
            nom="Test Contact User",
            carrec="Tester",
            email="test_contact@example.com",
            telefon="123456789"
        )
        
        print("Inserting contacte...")
        db.add(new_contacte)
        db.commit()
        db.refresh(new_contacte)
        print(f"Success! Inserted con ID: {new_contacte.id}")
        
    except Exception as e:
        import traceback
        print("Error encountered:")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_insert()
