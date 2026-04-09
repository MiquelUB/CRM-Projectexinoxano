
import os
import psycopg2
from dotenv import load_dotenv

# Carrega variables d'entorn
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def fix_database_v2_structure():
    try:
        print("FIX: Connectant a la base de dades per aplicar correccions V2...")
        # Intentem assegurar connexió directa si fos necessari (port 5432)
        url = DATABASE_URL
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()

        # 1. ASSEGURAR TAULA agent_memories_v2
        print("TABLE: Assegurant taula agent_memories_v2...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.agent_memories_v2 (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                municipi_id UUID NOT NULL REFERENCES public.municipis_lifecycle(id),
                usuari_id UUID REFERENCES public.usuaris(id),
                session_id UUID,
                expires_at TIMESTAMPTZ,
                history JSONB DEFAULT '[]',
                summary TEXT,
                clau VARCHAR(50),
                valor TEXT,
                confidenca FLOAT DEFAULT 1.0,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS ix_agent_memories_v2_session_id ON agent_memories_v2 (session_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_agent_memories_v2_clau ON agent_memories_v2 (clau);")

        # 2. ASSEGURAR TAULA activitats_municipi (Timeline)
        print("TABLE: Assegurant taula activitats_municipi...")
        # Ens assegurem que el tipus enum existeix
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
            CREATE TABLE IF NOT EXISTS public.activitats_municipi (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                municipi_id UUID NOT NULL REFERENCES public.municipis_lifecycle(id),
                contacte_id UUID REFERENCES public.contactes_v2(id),
                deal_id UUID REFERENCES public.deals(id),
                tipus_activitat tipus_activitat NOT NULL,
                data_activitat TIMESTAMPTZ DEFAULT NOW(),
                contingut JSONB DEFAULT '{}',
                notes_comercial TEXT,
                generat_per_ia BOOLEAN DEFAULT FALSE,
                etiquetes TEXT[] DEFAULT '{}',
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS ix_activitats_municipi_municipi_id ON activitats_municipi (municipi_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_activitats_municipi_tipus ON activitats_municipi (tipus_activitat);")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_activitats_municipi_data ON activitats_municipi (data_activitat);")

        # 3. FIX memoria_municipis (Afegir columnes tàctiques de Fase 2.2)
        print("COLUMN: Corregint taula memoria_municipis (Afegint resum_tactic)...")
        cols_to_add = [
            ("resum_tactic", "TEXT"),
            ("resum_setmanal", "JSONB DEFAULT '{}'"),
            ("data_resum", "TIMESTAMPTZ")
        ]
        for col_name, col_type in cols_to_add:
            cur.execute(f"""
                DO $$ BEGIN
                    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                                   WHERE TABLE_NAME = 'memoria_municipis' AND COLUMN_NAME = '{col_name}') THEN
                        ALTER TABLE public.memoria_municipis ADD COLUMN {col_name} {col_type};
                    END IF;
                END $$;
            """)

        # 4. ASSEGURAR TAULA tasques_v2
        print("TABLE: Assegurant taula tasques_v2...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.tasques_v2 (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                municipi_id UUID NOT NULL REFERENCES public.municipis_lifecycle(id),
                titol VARCHAR(200) NOT NULL,
                descripcio TEXT,
                data_venciment TIMESTAMPTZ,
                prioritat VARCHAR(20) DEFAULT 'mitjana',
                estat VARCHAR(20) DEFAULT 'pendent',
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)

        # 5. ASSEGURAR TAULA memoria_global
        print("TABLE: Assegurant taula memoria_global...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.memoria_global (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                categoria VARCHAR(50) NOT NULL,
                llico TEXT NOT NULL,
                evidencia JSONB DEFAULT '{}',
                confianca FLOAT DEFAULT 0.0,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)

        print("\nSUCCESS: ESTRUCTURA DE LA BASE DE DADES SINCRONITZADA AMB MODELS_V2!")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    fix_database_v2_structure()
