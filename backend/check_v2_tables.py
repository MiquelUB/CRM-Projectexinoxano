
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable")

def check_tables():
    tables = [
        "municipis_lifecycle", "contactes_v2", "email_drafts_v2", 
        "email_sequencies_v2", "emails_v2", "activitats_municipi", 
        "agent_memories_v2", "memoria_municipis", "tasques_v2", 
        "memoria_global", "patrons_municipis"
    ]
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        for t in tables:
            cur.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{t}');")
            exists = cur.fetchone()[0]
            print(f"Table '{t}': {'EXISTS' if exists else 'MISSING'}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_tables()
