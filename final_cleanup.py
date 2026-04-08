import csv
import psycopg2
import json

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def final_cleanup():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # 1. ALEMBIC VERSION
        print("🏗️ Configurant alembic_version...")
        cur.execute("CREATE TABLE IF NOT EXISTS public.alembic_version (version_num character varying NOT NULL PRIMARY KEY)")
        cur.execute("TRUNCATE TABLE public.alembic_version")
        with open("migracio_dades/alembic_version_rows.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("INSERT INTO public.alembic_version (version_num) VALUES (%s)", (row['version_num'],))

        # 2. MEMORIA MUNICIPIS
        print("🏗️ Carregant memoria_municipis...")
        cur.execute("TRUNCATE TABLE public.memoria_municipis CASCADE")
        with open("migracio_dades/memoria_municipis_rows.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            m_cols = ['municipi_id', 'ganxos_exitosos', 'angles_fallits', 'moment_optimal', 'llenguatge_preferit', 'blockers_resolts', 'data_actualitzacio']
            for row in reader:
                vals = []
                for c in m_cols:
                    val = row.get(c)
                    if val == '' or val is None: vals.append(None)
                    elif c in ['ganxos_exitosos', 'angles_fallits', 'moment_optimal', 'llenguatge_preferit', 'blockers_resolts']:
                        vals.append(val if val.strip() else '{}')
                    else: vals.append(val)
                
                phs = ", ".join(["%s"] * len(m_cols))
                cur.execute(f"INSERT INTO public.memoria_municipis ({', '.join(m_cols)}) VALUES ({phs})", vals)

        conn.commit()
        print("✨ ALEMBIC I MEMÒRIA CONFIGURATS AMB ÈXIT!")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    final_cleanup()
