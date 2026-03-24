import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
load_dotenv("backend/.env")

from database import SessionLocal
import models

def check_etapes():
    db = SessionLocal()
    try:
        deals = db.query(models.Deal).all()
        print(f"Total deals: {len(deals)}")
        for d in deals:
            print(f"Deal ID: {d.id} | Titulo: {d.titol} | Etapa: '{d.etapa}'")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_etapes()
