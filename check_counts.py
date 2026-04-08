import psycopg2

conn_str = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

tables_to_check = ['municipis', 'usuaris', 'contactes', 'deals', 'emails']

try:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    print("Estat actual de les dades a Easypanel:")
    for table in tables_to_check:
        cur.execute(f"SELECT COUNT(*) FROM public.{table}")
        count = cur.fetchone()[0]
        print(f"- {table}: {count} registres")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
