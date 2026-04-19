
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: DATABASE_URL no trobada.")
    exit(1)

engine = create_engine(DATABASE_URL)

def audit_db():
    queries = {
        "Total Municipis (Unified V2)": "SELECT count(*) FROM municipis",
        "Total Contactes": "SELECT count(*) FROM contactes",
        "Total Emails": "SELECT count(*) FROM emails",
        "Municipis per etapa": "SELECT etapa_actual, count(*) FROM municipis GROUP BY etapa_actual",
        "Emails vinculats a municipis": "SELECT count(*) FROM emails WHERE municipi_id IS NOT NULL",
        "Activitats totals": "SELECT count(*) FROM activitats",
        "Tasques pendents": "SELECT count(*) FROM tasques WHERE estat = 'pendent'",
        "Backups: Deals V1": "SELECT count(*) FROM deals_v1_backup",
        "Backups: Municipis V1": "SELECT count(*) FROM municipis_v1_backup"
    }
    
    with engine.connect() as conn:
        print("--- AUDITORIA ESTAT DE DADES CRM PXX ---")
        for desc, query in queries.items():
            try:
                result = conn.execute(text(query)).fetchone()
                print(f"[OK] {desc}: {result[0]}")
                conn.commit()
            except Exception as e:
                print(f"[ERROR] {desc}: {e}")
                conn.rollback()

if __name__ == "__main__":
    audit_db()
