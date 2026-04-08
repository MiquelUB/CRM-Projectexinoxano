import psycopg2

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def check_structure():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'municipis' AND table_schema = 'public'")
        cols = cur.fetchall()
        print("COLUMNS IN DB:")
        for c in cols:
            print(f" - {c[0]} ({c[1]})")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_structure()
