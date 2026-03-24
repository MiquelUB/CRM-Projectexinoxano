import os
import re
import psycopg2

# URL de la base de dades intern d'Easypanel
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://pxx_admin:b86f95465942a859661e@crmpxx_db-crmpxx:5432/crm_pxx?sslmode=disable"
)

# Ara que està dins de backend/, el fitxer estarà al mateix directori
SQL_FILE = "dades_inserts.sql"

def execute_statements():
    if not os.path.exists(SQL_FILE):
        print(f"❌ Error: No s'ha trobat el fitxer {SQL_FILE}")
        return

    print(f"🔄 Llegint fitxer {SQL_FILE}...")
    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql_content = f.read()

    print(f"🔌 Connectant a la base de dades...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        cur = conn.cursor()

        print("✅ Connexió establerta! Desactivant 'triggers' i claus foranes...")
        cur.execute("SET session_replication_role = 'replica';")

        statements = sql_content.split(";\n")
        total = len(statements)
        success_count = 0
        error_count = 0

        print(f"🚀 Iniciant importació de {total} instruccions...")
        
        for i, stmt in enumerate(statements):
            stmt = stmt.strip()
            if not stmt or stmt.startswith("--"):
                continue

            try:
                cur.execute(stmt + ";")
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"⚠️ Error a la línia aproximada {i+1}: {str(e)[:150]}...")
                conn.rollback()
                print("❌ Aturant per error. Revisa el format. Fent Rollback.")
                return

        cur.execute("SET session_replication_role = 'origin';")
        conn.commit()
        
        print("\n" + "="*40)
        print(f"🎉 IMPORTACIÓ FINALITZADA!")
        print(f"✅ Executats amb èxit: {success_count}")
        print(f"⚠️ Errors: {error_count}")
        print("="*40)

    except Exception as e:
        print(f"❌ Error critic connectant a la base de dades: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    execute_statements()
