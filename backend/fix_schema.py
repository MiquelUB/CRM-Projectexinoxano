import psycopg2
import os
import sys
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("FATAL: DATABASE_URL no definida! Aturant fix_schema.")
    sys.exit(1)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def fix_db_schema():
    print(f"Connexi a la base de dades per correcci de schema...")
    
    conn = None
    cur = None
    
    try:
        # Connexió amb autocommit per evitar problemes de transaccions amb DDL
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True  # CLAU: Cada operació DDL es commiteja automàticament
        cur = conn.cursor()
        
        # 1. Assegurar Extensions
        print(" creant extensions necessàries...")
        cur.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
        
        # 2. Verificar si municipis existeix abans d'afegir columnes
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'municipis'
            );
        """)
        
        if cur.fetchone()[0]:
            print(" Verificant existència de columnes a municipis...")
            
            # Verificar si usuari_asignat ja existeix
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='municipis' 
                  AND column_name='usuari_asignat'
            """)
            
            if not cur.fetchone():
                print(" Afegint columna usuari_asignat a municipis...")
                cur.execute("""
                    ALTER TABLE public.municipis 
                    ADD COLUMN usuari_asignat VARCHAR(50);
                """)
            else:
                print(" Columna usuari_asignat ja existeix")
        else:
            print(" Taula municipis no existeix encara (Alembic la crearà)")
        
        print(" Correcció de schema finalitzada (control passat a Alembic).")
        
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
