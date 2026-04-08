import json
import psycopg2

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"
FILE_PATH = "migracio_dades/minicipis"

def fresh_start():
    try:
        # 1. Llegir dades
        print(f"📖 Llegint {FILE_PATH}...")
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.endswith('.'): content = content[:-1]
            data = json.loads(content)
        
        # 2. Connectar i Recrear
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("🔥 Esborrant taula municipis (CASCADE)...")
        cur.execute("DROP TABLE IF EXISTS public.municipis CASCADE")
        
        print("🏗️ Creant taula municipis de bell nou...")
        cur.execute("""
            CREATE TABLE public.municipis (
              id uuid NOT NULL,
              nom character varying NOT NULL,
              tipus character varying NOT NULL,
              provincia character varying,
              poblacio character varying,
              web character varying,
              telefon character varying,
              adreca text,
              notes text,
              created_at timestamp with time zone DEFAULT now(),
              updated_at timestamp with time zone DEFAULT now(),
              codi_postal character varying,
              CONSTRAINT municipis_pkey PRIMARY KEY (id)
            )
        """)
        
        # 3. Inserir dades
        colnames = ['id', 'nom', 'tipus', 'provincia', 'poblacio', 'web', 'telefon', 'adreca', 'notes', 'created_at', 'updated_at', 'codi_postal']
        
        print(f"📥 Injectant {len(data)} municipis...")
        for obj in data:
            values = [obj.get(c) for c in colnames]
            placeholders = ", ".join(["%s"] * len(colnames))
            cur.execute(f"INSERT INTO public.municipis ({', '.join([f'\"{c}\"' for c in colnames])}) VALUES ({placeholders})", values)
        
        conn.commit()
        print("✨ FRESH START COMPLETAT AMB ÈXIT!")
        
        # Verificar count final
        cur.execute("SELECT COUNT(*) FROM public.municipis")
        print(f"📊 Registres totals ara: {cur.fetchone()[0]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    fresh_start()
