
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable")

def check_all_tables():
    tables_to_check = [
        # V1
        "usuaris", "municipis", "contactes", "deals", "emails", 
        "llicencies", "pagaments", "tasques", "deal_activitats", "agent_memories",
        # V2
        "municipis_lifecycle", "contactes_v2", "emails_v2", "tasques_v2", 
        "activitats_municipi", "agent_memories_v2", "memoria_municipis", "memoria_global",
        "patrons_municipi"
    ]
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print(f"CONNECTAT A: {DATABASE_URL.split('@')[-1]}")
        print("-" * 50)
        
        missing = []
        for table in tables_to_check:
            try:
                cur.execute(f"SELECT 1 FROM {table} LIMIT 1")
                print(f"[OK] Taula '{table}' existeix.")
            except psycopg2.errors.UndefinedTable:
                conn.rollback()
                print(f"[MISSING] Taula '{table}' NO EXISTEIX.")
                missing.append(table)
            except Exception as e:
                conn.rollback()
                print(f"[ERROR] Taula '{table}': {e}")
        
        print("-" * 50)
        if missing:
            print(f"FALTEN {len(missing)} TAULES: {', '.join(missing)}")
        else:
            print("TOTES LES TAULES ESTAN PRESENTS!")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR CONNECTANT: {e}")

if __name__ == "__main__":
    check_all_tables()
