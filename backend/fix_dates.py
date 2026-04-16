
import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

def fix_email_dates():
    db = SessionLocal()
    try:
        print("Buscant emails amb dates invàlides...")
        emails = db.query(models.Email).all()
        count = 0
        for em in emails:
            # Si la data_enviament és NULL, posem la data de creació o la d'ara
            if not em.data_enviament:
                em.data_enviament = datetime.now(timezone.utc)
                count += 1
        
        db.commit()
        print(f"S'han reparat {count} emails.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_email_dates()
