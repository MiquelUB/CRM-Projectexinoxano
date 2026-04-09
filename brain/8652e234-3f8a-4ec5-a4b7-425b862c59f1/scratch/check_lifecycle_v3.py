import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('backend/.env')
DATABASE_URL = os.getenv("DATABASE_URL")

def check_lifecycle_data():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    try:
        print("Checking municipis_lifecycle columns and sample data...")
        cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'municipis_lifecycle';")
        cols = cur.fetchall()
        for col in cols:
            print(f"Column: {col[0]}, Type: {col[1]}")
            
        cur.execute("SELECT id, etapa_actual, valor_setup, valor_llicencia FROM municipis_lifecycle LIMIT 5;")
        rows = cur.fetchall()
        print("\nSample Rows:")
        for row in rows:
            print(row)
            
        cur.execute("SELECT COUNT(*) FROM municipis_lifecycle WHERE etapa_actual IS NULL;")
        null_etapa = cur.fetchone()[0]
        print(f"\nRows with NULL etapa_actual: {null_etapa}")
        
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    check_lifecycle_data()
