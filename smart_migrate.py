import psycopg2
from psycopg2.extras import execute_values

SUPABASE_URL = "postgresql://postgres.qyfyyrhwwzkohljxpimj:o%3EDi5W%3CP%3CZEeE5pjcHYpdTi2r@aws-1-eu-west-1.pooler.supabase.com:6543/postgres"
EASYPANEL_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

# Ordre d'importació per respectar claus foranes
TABLES = [
    'usuaris',
    'municipis',
    'contactes',
    'municipis_lifecycle',
    'contactes_v2',
    'deals',
    'deal_activitats',
    'emails',
    'tasques',
    'patrons_municipis',
    'emails_v2',
    'memoria_municipis',
    'reunions_v2',
    'trucades_v2',
    'email_drafts_v2',
    'email_sequencies_v2'
]

def smart_migrate():
    try:
        print("🔗 Connectant a les bases de dades...")
        s_conn = psycopg2.connect(SUPABASE_URL)
        e_conn = psycopg2.connect(EASYPANEL_URL)
        s_cur = s_conn.cursor()
        e_cur = e_conn.cursor()

        print("🚀 Iniciant còpia de dades taula per taula...")

        for table in TABLES:
            print(f"\nProcessing table: {table}")
            
            # 1. Llegir de Supabase
            try:
                s_cur.execute(f"SELECT * FROM public.{table}")
                rows = s_cur.fetchall()
                colnames = [desc[0] for desc in s_cur.description]
                print(f"  📥 Llegits {len(rows)} registres de Supabase.")
            except Exception as e:
                print(f"  ⚠️ Error llegint {table} de Supabase (potser no existeix): {e}")
                s_conn.rollback()
                continue

            if not rows:
                print(f"  ℹ️ Taula buida, saltant...")
                continue

            # 2. Netejar Easypanel
            try:
                e_cur.execute(f"TRUNCATE TABLE public.{table} RESTART IDENTITY CASCADE;")
            except Exception as e:
                print(f"  ⚠️ Error netejant {table} a Easypanel: {e}")
                e_conn.rollback()
                continue

            # 3. Inserir a Easypanel
            try:
                from psycopg2.extras import Json
                
                # Adaptar dades (convertir dicts i lists a Json per a JSONB)
                adapted_rows = []
                for row in rows:
                    new_row = []
                    for val in row:
                        if isinstance(val, (dict, list)):
                            new_row.append(Json(val))
                        else:
                            new_row.append(val)
                    adapted_rows.append(tuple(new_row))

                columns = ", ".join(colnames)
                query = f"INSERT INTO public.{table} ({columns}) VALUES %s"
                
                execute_values(e_cur, query, adapted_rows)
                print(f"  ✅ {len(rows)} registres migrats correctament.")
            except Exception as e:
                print(f"  ❌ Error inserint dades a {table}: {e}")
                e_conn.rollback()
                continue

            e_conn.commit()

        print("\n✨ MIGRACIÓ DIRECTA COMPLETADA AMB ÈXIT!")
        
        s_cur.close()
        e_cur.close()
        s_conn.close()
        e_conn.close()

    except Exception as e:
        print(f"💥 Error crític: {e}")

if __name__ == "__main__":
    smart_migrate()
