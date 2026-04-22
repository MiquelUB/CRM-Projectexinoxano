from database import SessionLocal
from sqlalchemy import text
import traceback

def check():
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'"))
        tables = [r[0] for r in result.fetchall()]
        print("Existing tables:", tables)
        
        critical_tables = ["activitats_municipi", "municipis_lifecycle"]
            if t in tables:
                print(f"✅ Table {t} exists.")
            else:
                print(f"❌ Table {t} MISSING!")
    except Exception as e:
        print("Error checking tables:")
        traceback.print_exc()

if __name__ == "__main__":
    check()
