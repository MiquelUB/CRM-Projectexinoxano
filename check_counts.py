import psycopg2

conn_str = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

tables_v2 = ['municipis_lifecycle', 'contactes_v2', 'tasques_v2', 'emails_v2']
tables_legacy = ['_legacy_municipis', '_legacy_contactes', '_legacy_deals']

try:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    print("=== ESTAT DE LA BASE DE DADES (V2) ===")
    for table in tables_v2:
        try:
            cur.execute(f"SELECT COUNT(*) FROM public.{table}")
            count = cur.fetchone()[0]
            print(f"- {table}: {count} registres")
        except:
            conn.rollback()
            print(f"- {table}: NO EXISTEIX")

    print("\n=== ESTAT DE LA BASE DE DADES (LEGACY V1) ===")
    for table in tables_legacy:
        try:
            cur.execute(f"SELECT COUNT(*) FROM public.{table}")
            count = cur.fetchone()[0]
            print(f"- {table}: {count} registres")
        except:
            conn.rollback()
            print(f"- {table}: NO EXISTEIX")
            
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
