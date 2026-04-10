
from database import SessionLocal
from sqlalchemy import text
import uuid

def search():
    db = SessionLocal()
    try:
        print("--- SEARCHING FOR ISONA ---")
        # Search in Municipis (V1)
        r1 = db.execute(text("SELECT id, nom FROM municipis WHERE nom ILIKE '%Isona%'")).fetchall()
        print(f"V1 Municipis: {r1}")
        
        # Search in MunicipisLifecycle (V2)
        r2 = db.execute(text("SELECT id, nom FROM municipis_lifecycle WHERE nom ILIKE '%Isona%'")).fetchall()
        print(f"V2 Municipis: {r2}")
        
        # Search in Deals (V1)
        r3 = db.execute(text("SELECT id, titol, municipi_id FROM deals WHERE titol ILIKE '%Isona%'")).fetchall()
        print(f"V1 Deals: {r3}")
        
        # Search in Emails linked to Isona
        if r2:
            m_id = r2[0][0]
            r4 = db.execute(text(f"SELECT count(*) FROM emails e JOIN deals d ON e.deal_id = d.id WHERE d.municipi_id = '{m_id}'")).scalar()
            print(f"Emails linked to Isona ({m_id}): {r4}")
            
            # Check activities
            r5 = db.execute(text(f"SELECT count(*) FROM activitats_municipi WHERE municipi_id = '{m_id}'")).scalar()
            print(f"Activities linked to Isona: {r5}")
            
    finally:
        db.close()

if __name__ == "__main__":
    search()
