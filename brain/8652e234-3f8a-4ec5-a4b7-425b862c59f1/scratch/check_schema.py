import psycopg2

conn_str = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

try:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    
    # 1. Check municipis_lifecycle
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'municipis_lifecycle' ORDER BY column_name")
    cols = [c[0] for c in cur.fetchall()]
    print("--- COLUMNS IN municipis_lifecycle ---")
    print(cols)
    
    # 2. Check stages of data
    cur.execute("SELECT nom, etapa_actual FROM municipis_lifecycle LIMIT 10")
    data = cur.fetchall()
    print("\n--- DATA SAMPLES ---")
    for d in data:
        print(f"{d[0]}: {d[1]}")
        
    cur.close()
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
