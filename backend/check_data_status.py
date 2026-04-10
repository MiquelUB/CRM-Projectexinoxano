
import os
from sqlalchemy import create_url, create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: DATABASE_URL no trobada.")
    exit(1)

engine = create_engine(DATABASE_URL)

def audit_db():
    queries = {
        "Total Deals (V1)": "SELECT count(*) FROM deals",
        "Total MunicipiLifecycle (V2)": "SELECT count(*) FROM municipis_lifecycle",
        "Deals per etapa": "SELECT etapa, count(*) FROM deals GROUP BY etapa",
        "Deals sense municipi_id": "SELECT count(*) FROM deals WHERE municipi_id IS NULL",
        "Emails totals": "SELECT count(*) FROM emails",
        "Emails vinculats a deals": "SELECT count(*) FROM emails WHERE deal_id IS NOT NULL",
        "Activitats V2": "SELECT count(*) FROM activitats_municipi"
    }
    
    with engine.connect() as conn:
        print("--- AUDITORIA ESTAT DE DADES ---")
        for desc, query in queries.items():
            try:
                result = conn.execute(text(query)).fetchone()
                print(f"{desc}: {result[0]}")
            except Exception as e:
                print(f"{desc}: ERROR -> {e}")

if __name__ == "__main__":
    audit_db()
