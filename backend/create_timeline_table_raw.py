
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_table_raw():
    # Eliminem el paràmetre ssl si dóna problemes o el configurem
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Connectat per crear taula...")
        
        # 1. Crear el tipus ENUM si no existeix
        conn.execute(text("""
            DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipus_activitat') THEN
                    CREATE TYPE tipus_activitat AS ENUM (
                        'nota_manual', 'email_enviat', 'email_rebut', 'trucada', 
                        'reunio', 'demo', 'pagament', 'canvi_etapa', 'sistema'
                    );
                END IF;
            END $$;
        """))
        
        # 2. Crear la taula activitats_municipi
        conn.execute(text("""
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
        """))
        conn.commit()
        print("Taula activitats_municipi creada amb èxit (SQL RAW).")

if __name__ == "__main__":
    create_table_raw()
