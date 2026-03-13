import psycopg2
import sys

def test_conn():
    host = "aws-1-eu-west-1.pooler.supabase.com"
    password = "o>Di5W<P<ZEeE5pjcHYpdTi2r"
    user = "postgres.qyfyyrhwwzkohljxpimj"
    print(f"Testing {host}...")
    try:
        conn = psycopg2.connect(
            host=host,
            database="postgres",
            user=user,
            password=password,
            port=6543,
            connect_timeout=5
        )
        print("SUCCESS!")
        conn.close()
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_conn()
