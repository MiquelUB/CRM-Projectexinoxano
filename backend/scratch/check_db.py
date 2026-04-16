import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from sqlalchemy import text

def check_db():
    db = SessionLocal()
    try:
        tables = ["municipis", "tasques", "emails", "contactes", "activitats", "llicencies", "pagaments"]
        for table in tables:
            try:
                count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                print(f"Table {table}: {count} rows")
            except Exception as e:
                print(f"Table {table}: Error checking - {e}")
                
        # Also check for legacy tables
        legacy_tables = ["municipis_v2", "municipis_lifecycle", "deals"]
        for table in legacy_tables:
            try:
                count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                print(f"Legacy Table {table}: {count} rows")
            except Exception:
                pass # Legacy table doesn't exist, which is fine
                
    finally:
         db.close()

if __name__ == "__main__":
    check_db()
