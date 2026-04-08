import csv
import psycopg2

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"
FILE_PATH = "migracio_dades/Usuaris"

def fresh_start_usuaris():
    try:
        print(f"📖 Llegint {FILE_PATH} (CSV)...")
        data = []
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Eliminem punts finals que puguin venir d'un copy-paste
            if content.endswith('.'): content = content[:-1]
            
            from io import StringIO
            f_fake = StringIO(content)
            reader = csv.DictReader(f_fake)
            for row in reader:
                data.append(row)
        
        print(f"👀 Files detectades: {len(data)}")
        if data:
            print(f"  Primer usuari: {data[0].get('email')}")
        
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("🔥 Esborrant taula usuaris (CASCADE)...")
        cur.execute("DROP TABLE IF EXISTS public.usuaris CASCADE")
        
        print("🏗️ Creant taula usuaris de bell nou...")
        cur.execute("""
            CREATE TABLE public.usuaris (
              id uuid NOT NULL,
              email character varying NOT NULL UNIQUE,
              password_hash character varying NOT NULL,
              nom character varying NOT NULL,
              rol character varying,
              actiu boolean,
              created_at timestamp with time zone DEFAULT now(),
              updated_at timestamp with time zone DEFAULT now(),
              CONSTRAINT usuaris_pkey PRIMARY KEY (id)
            )
        """)
        
        colnames = ['id', 'email', 'password_hash', 'nom', 'rol', 'actiu', 'created_at', 'updated_at']
        
        print(f"📥 Injectant {len(data)} usuari/s...")
        for row in data:
            # Convertim 'true'/'false' de string a bool de Python
            if 'actiu' in row:
                row['actiu'] = row['actiu'].lower() == 'true'
            
            values = [row.get(c) for c in colnames]
            placeholders = ", ".join(["%s"] * len(colnames))
            cur.execute(f"INSERT INTO public.usuaris ({', '.join([f'\"{c}\"' for c in colnames])}) VALUES ({placeholders})", values)
        
        conn.commit()
        print("✨ FRESH START USUARIS COMPLETAT AMB ÈXIT!")
        
        cur.execute("SELECT COUNT(*) FROM public.usuaris")
        print(f"📊 Registres totals ara: {cur.fetchone()[0]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    fresh_start_usuaris()
