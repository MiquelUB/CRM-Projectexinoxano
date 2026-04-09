
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Canviem el port a 5432 per a la migració (Supabase direct)
DATABASE_URL = os.getenv("DATABASE_URL").replace(":6543/", ":5432/")

def create_table_direct():
    try:
        print(f"Intentant connexió directa a 5432...")
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute("SELECT version();")
        print(f"Versió DB: {cur.fetchone()}")

        cur.execute("""
            DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipus_activitat') THEN
                    CREATE TYPE tipus_activitat AS ENUM (
                        'nota_manual', 'email_enviat', 'email_rebut', 'trucada', 
                        'reunio', 'demo', 'pagament', 'canvi_etapa', 'sistema'
                    );
                END IF;
            END $$;
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS activitats_municipi (
                id UUID PRIMARY KEY,
                municipi_id UUID NOT NULL,
                contacte_id UUID,
                deal_id UUID,
                tipus_activitat tipus_activitat NOT NULL,
                data_activitat TIMESTAMPTZ DEFAULT NOW(),
                contingut JSONB DEFAULT '{}',
                notes_comercial TEXT,
                generat_per_ia BOOLEAN DEFAULT FALSE,
                etiquetes TEXT[] DEFAULT '{}'
            );
        """)
        print("Taula activitats_municipi creada amb èxit (PSQL Direct Port 5432).")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error en connexió directa: {e}")

if __name__ == "__main__":
    create_table_direct()
