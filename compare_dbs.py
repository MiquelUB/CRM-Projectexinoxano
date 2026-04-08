import psycopg2

SUPABASE_URL = "postgresql://postgres.qyfyyrhwwzkohljxpimj:o%3EDi5W%3CP%3CZEeE5pjcHYpdTi2r@aws-1-eu-west-1.pooler.supabase.com:6543/postgres"
EASYPANEL_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

TABLES = ['usuaris', 'municipis', 'contactes', 'deals', 'emails']

def compare_dbs():
    try:
        s_conn = psycopg2.connect(SUPABASE_URL)
        e_conn = psycopg2.connect(EASYPANEL_URL)
        s_cur = s_conn.cursor()
        e_cur = e_conn.cursor()

        print(f"{'Taula':<20} | {'Supabase':<10} | {'Easypanel':<10}")
        print("-" * 45)

        for table in TABLES:
            s_cur.execute(f"SELECT COUNT(*) FROM public.{table}")
            s_count = s_cur.fetchone()[0]
            
            e_cur.execute(f"SELECT COUNT(*) FROM public.{table}")
            e_count = e_cur.fetchone()[0]
            
            print(f"{table:<20} | {s_count:<10} | {e_count:<10}")

        s_cur.close()
        e_cur.close()
        s_conn.close()
        e_conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compare_dbs()
