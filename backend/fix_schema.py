import pg8000.native
import os
import sys
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("FATAL: DATABASE_URL no definida! Aturant fix_schema.")
    sys.exit(1)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def fix_db_schema():
    print(f"Connexió a la base de dades per correcció de schema (usant pg8000)...")
    
    conn = None
    
    try:
        # Parse DATABASE_URL for pg8000
        url = urlparse(DATABASE_URL)
        
        conn = pg8000.native.Connection(
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
            database=url.path[1:]
        )
        
        # 1. Assegurar Extensions
        print(" creant extensions necessàries...")
        conn.run('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
        
        # 2. Verificar si municipis existeix
        res = conn.run("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'municipis'
            );
        """)
        
        if res[0][0]:
            print(" Verificant existència de columnes a municipis...")
            # Verificar si usuari_asignat ja existeix
            col_res = conn.run("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='municipis' 
                  AND column_name='usuari_asignat'
            """)
            
            if not col_res:
                print(" Afegint columna usuari_asignat a municipis...")
                conn.run("ALTER TABLE public.municipis ADD COLUMN usuari_asignat VARCHAR(50);")
            else:
                print(" Columna usuari_asignat ja existeix")
        else:
            print(" Taula municipis no existeix encara")
        
        print(" Correcció de schema finalitzada.")
        
    except Exception as e:
        print(f" Error corregint schema: {e}")
        print(" Continuant amb el procés...")
        
    finally:
        if conn:
            try:
                conn.close()
                print(" Connexió tancada correctament")
            except: pass

if __name__ == "__main__":
    fix_db_schema()

if __name__ == "__main__":
    fix_db_schema()
