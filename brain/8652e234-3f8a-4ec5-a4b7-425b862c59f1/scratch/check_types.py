import psycopg2

conn_str = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

try:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    
    # Check enum types
    cur.execute("SELECT n.nspname as schema, t.typname as type FROM pg_type t JOIN pg_namespace n ON n.oid = t.typnamespace WHERE t.typtype = 'e'")
    enums = cur.fetchall()
    print("--- ENUM TYPES ---")
    for e in enums:
        print(f"{e[0]}.{e[1]}")
        
    # Check column types in municipis_lifecycle
    cur.execute("SELECT column_name, data_type, udt_name FROM information_schema.columns WHERE table_name = 'municipis_lifecycle'")
    cols = cur.fetchall()
    print("\n--- COLUMN TYPES ---")
    for c in cols:
        print(f"{c[0]}: {c[1]} ({c[2]})")
        
    cur.close()
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
