import psycopg2
import sys

conn_str = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

try:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
    tables = cur.fetchall()
    
    print("--- TABLES IN PUBLIC SCHEMA ---")
    if not tables:
        print("EMPTY SCHEMA!")
    for t in tables:
        # Check count for each table
        cur.execute(f'SELECT COUNT(*) FROM "{t[0]}"')
        count = cur.fetchone()[0]
        print(f"- {t[0]}: {count} rows")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"CONNECTION ERROR: {e}")
