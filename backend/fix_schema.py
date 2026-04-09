import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pxx_admin:b86f95465942a859661e@crmpxx_db-crmpxx:5432/crm_pxx?sslmode=disable")

def fix_db_schema():
    print(f"Connexi a la base de dades per correcci de schema...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # 1. Assegurar Extensions
        cur.execute("CREATE EXTENSION IF NOT EXISTS \"pgcrypto\";")
        
        # 2. Només mantenim correccions de columnes crítiques si falten en taules base
        # Però NO creem taules V2 manualment, deixem que Alembic ho faci.
        
        # Verifiquem si municipis_lifecycle existeix abans d'afegir la columna
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'municipis_lifecycle');")
        if cur.fetchone()[0]:
            print("🔍 Verificant existència de columnes a municipis_lifecycle...")
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='municipis_lifecycle' AND column_name='usuari_asignat'
            """)
            if not cur.fetchone():
                print("➕ Afegint columna usuari_asignat a municipis_lifecycle...")
                cur.execute("ALTER TABLE public.municipis_lifecycle ADD COLUMN usuari_asignat VARCHAR(50);")

        conn.commit()
        print("✅ Correcció de schema finalitzada (control passat a Alembic).")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error corregint schema: {e}")

if __name__ == "__main__":
    fix_db_schema()
