import csv
import psycopg2
from io import StringIO

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"
FILE_PATH = "migracio_dades/contactes"

def fresh_start_contactes():
    try:
        print(f"📖 Llegint {FILE_PATH} (CSV)...")
        data = []
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.endswith('.'): content = content[:-1]
            
            f_fake = StringIO(content)
            reader = csv.DictReader(f_fake)
            for row in reader:
                data.append(row)
        
        print(f"👀 Files detectades: {len(data)}")
        
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("🔥 Esborrant taula contactes (CASCADE)...")
        cur.execute("DROP TABLE IF EXISTS public.contactes CASCADE")
        
        print("🏗️ Creant taula contactes de bell nou...")
        cur.execute("""
            CREATE TABLE public.contactes (
              id uuid NOT NULL,
              municipi_id uuid NOT NULL,
              nom character varying NOT NULL,
              carrec character varying,
              email character varying,
              telefon character varying,
              linkedin character varying,
              notes_humanes text,
              actiu boolean,
              created_at timestamp with time zone DEFAULT now(),
              updated_at timestamp with time zone DEFAULT now(),
              CONSTRAINT contactes_pkey PRIMARY KEY (id),
              CONSTRAINT contactes_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis(id)
            )
        """)
        
        colnames = ['id', 'municipi_id', 'nom', 'carrec', 'email', 'telefon', 'linkedin', 'notes_humanes', 'actiu', 'created_at', 'updated_at']
        
        print(f"📥 Injectant {len(data)} contactes...")
        for row in data:
            # Neteja de camps buits i booleans
            if 'actiu' in row:
                row['actiu'] = row['actiu'].lower() == 'true'
            
            # Si un camp és buit o només espais, el posem a None (NULL a SQL)
            for c in colnames:
                if row.get(c) == '':
                    row[c] = None
                elif isinstance(row.get(c), str):
                    row[c] = row[c].strip()

            values = [row.get(c) for c in colnames]
            placeholders = ", ".join(["%s"] * len(colnames))
            cur.execute(f"INSERT INTO public.contactes ({', '.join([f'\"{c}\"' for c in colnames])}) VALUES ({placeholders})", values)
        
        conn.commit()
        print("✨ FRESH START CONTACTES COMPLETAT AMB ÈXIT!")
        
        cur.execute("SELECT COUNT(*) FROM public.contactes")
        print(f"📊 Registres totals ara: {cur.fetchone()[0]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    fresh_start_contactes()
