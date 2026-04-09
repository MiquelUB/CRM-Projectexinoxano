
import os
import psycopg2
from dotenv import load_dotenv
import uuid

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_table_psycopg2():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        print("Connectat amb psycopg2...")

        # 1. Crear el tipus ENUM si no existeix
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
        
        # 2. Crear la taula activitats_municipi
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
        print("Taula activitats_municipi creada amb èxit (psycopg2).")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error amb psycopg2: {e}")

if __name__ == "__main__":
    create_table_psycopg2()
