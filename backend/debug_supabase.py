import socket
import psycopg2
import sys

def test_dns_and_conn(host, password):
    print(f"--- Testing Host: {host} ---")
    try:
        ip = socket.gethostbyname(host)
        print(f"IP resolved: {ip}")
    except Exception as e:
        print(f"DNS resolution failed: {e}")
        return False

    try:
        print(f"Trying connection with password: {password}...")
        conn = psycopg2.connect(
            host=host,
            database="postgres",
            user="postgres",
            password=password,
            port="5432",
            connect_timeout=5
        )
        print("SUCCESS! Connected to Supabase.")
        conn.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    host = "db.qyfyyrhwwzkohljxpimj.supabase.co"
    passwords = ["pxx_admin_2026!", "crm_xinoxano", "pxx_secret_local"]
    
    for pwd in passwords:
        if test_dns_and_conn(host, pwd):
            print(f"FOUND PASSWORD: {pwd}")
            sys.exit(0)
    
    print("Could not connect with any known passwords.")
    sys.exit(1)
