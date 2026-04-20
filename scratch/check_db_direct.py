
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
DB_URL = os.getenv("DATABASE_URL")

def get_count(table_name):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute(f"SELECT count(*) FROM {table_name}")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    tables = ['municipis', 'municipis_v1_backup', 'contactes', 'contactes_v1_backup', 'deals_v1_backup']
    for t in tables:
        print(f"Count for {t}: {get_count(t)}")
