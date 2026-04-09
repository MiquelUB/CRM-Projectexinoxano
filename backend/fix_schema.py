import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://pxx_admin:b86f95465942a859661e@crmpxx_db-crmpxx:5432/crm_pxx?sslmode=disable"
)

def fix_db():
    print("Connecting to DB...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Checking schemas...")
    cur.execute("SELECT schema_name FROM information_schema.schemata;")
    schemas = [row[0] for row in cur.fetchall()]
    print("Schemas existents:", schemas)
    
    if 'public' not in schemas:
        print("Creating public schema...")
        cur.execute("CREATE SCHEMA public;")
        print("Schema public created.")
    
    print("Granting permissions...")
    cur.execute("GRANT ALL ON SCHEMA public TO current_user;")
    cur.execute("GRANT ALL ON SCHEMA public TO public;")
    print("Permissions granted.")
    
    # 3. Crear taules estratègiques (Timeline i Agent)
    print("Verificant taules d'IA i Timeline...")
    
    # Enum activitats
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
    
    # Taula activitats
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

    # Taula Agent Memòries (per si no existís)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS agent_memories (
            id UUID PRIMARY KEY,
            usuari_id UUID NOT NULL,
            deal_id UUID,
            municipi_id UUID,
            history JSONB DEFAULT '[]',
            summary TEXT,
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    
    # Taula Tasques V2
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasques_v2 (
            id UUID PRIMARY KEY,
            municipi_id UUID NOT NULL REFERENCES municipis_lifecycle(id),
            usuari_id UUID REFERENCES usuaris(id),
            titol VARCHAR(300) NOT NULL,
            descripcio TEXT,
            data_venciment DATE NOT NULL,
            tipus VARCHAR(50) DEFAULT 'altre',
            prioritat VARCHAR(20) DEFAULT 'mitjana',
            estat VARCHAR(20) DEFAULT 'pendent',
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    
    print("Base de dades fixada i actualitzada per a Kimi K2 (Inclou Tasques V2).")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    fix_db()
