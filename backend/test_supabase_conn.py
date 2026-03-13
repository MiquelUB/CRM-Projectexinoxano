import psycopg2
import sys

def test_supabase_connection(password):
    host = "db.qyfyyrhwwzkohljxpimj.supabase.co"
    database = "postgres"
    user = "postgres"
    port = "5432"
    
    print(f"Testing connection to {host} with password: {password}...")
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port,
            connect_timeout=5
        )
        print("SUCCESS! Connected to Supabase.")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    passwords_to_try = [
        "pxx_admin_2026!",
        "crm_xinoxano",
        "pxx_secret_local"
    ]
    
    for pwd in passwords_to_try:
        if test_supabase_connection(pwd):
            sys.exit(0)
    sys.exit(1)
