import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pxx_admin:b86f95465942a859661e@crmpxx_db-crmpxx:5432/crm_pxx?sslmode=disable")

def fix_db_schema():
    print(f"Connexi a la base de dades per correcci de schema...")
    
    conn = None
    cur = None
    
    try:
        # Connexi amb autocommit per evitar problemes de transaccions amb DDL
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True  #  CLAU: Cada operaci DDL es commiteja automticament
        cur = conn.cursor()
        
        # 1. Assegurar Extensions
        print(" creant extensions necessries...")
        cur.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
        
        # 2. Verificar si municipis_lifecycle existeix abans d'afegir columnes
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'municipis_lifecycle'
            );
        """)
        
        if cur.fetchone()[0]:
            print(" Verificant existncia de columnes a municipis_lifecycle...")
            
            # Verificar si usuari_asignat ja existeix
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='municipis_lifecycle' 
                  AND column_name='usuari_asignat'
            """)
            
            if not cur.fetchone():
                print(" Afegint columna usuari_asignat a municipis_lifecycle...")
                cur.execute("""
                    ALTER TABLE public.municipis_lifecycle 
                    ADD COLUMN usuari_asignat VARCHAR(50);
                """)
            else:
                print(" Columna usuari_asignat ja existeix")
        else:
            print(" Taula municipis_lifecycle no existeix encara (Alembic la crear)")
        
        print(" Correcci de schema finalitzada (control passat a Alembic).")
        
    except Exception as e:
        print(f" Error corregint schema: {e}")
        print(" Continuant amb el procs (Alembic pot gestionar-ho)...")
        # No propagar l'error - deixar que el procs continu
        
    finally:
        #  CLAU: Tancar SEMPRE la connexi, passi el que passi
        if cur:
            cur.close()
        if conn:
            conn.close()
            print(" Connexi tancada correctament")

if __name__ == "__main__":
    fix_db_schema()
