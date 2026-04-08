import csv
import psycopg2
from io import StringIO

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"
FILE_PATH = "migracio_dades/deals_rows.csv"

def fresh_start_deals():
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
        
        print("🔥 Esborrant taula deals (CASCADE)...")
        cur.execute("DROP TABLE IF EXISTS public.deals CASCADE")
        
        print("🏗️ Creant taula deals de bell nou...")
        cur.execute("""
            CREATE TABLE public.deals (
              id uuid NOT NULL,
              municipi_id uuid NOT NULL,
              contacte_id uuid,
              titol character varying NOT NULL,
              etapa character varying NOT NULL,
              valor_setup numeric,
              valor_llicencia numeric,
              prioritat character varying,
              notes_humanes text,
              proper_pas text,
              data_seguiment date,
              data_tancament_prev date,
              data_tancament_real date,
              motiu_perdua text,
              created_at timestamp with time zone DEFAULT now(),
              updated_at timestamp with time zone DEFAULT now(),
              CONSTRAINT deals_pkey PRIMARY KEY (id),
              CONSTRAINT deals_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes(id),
              CONSTRAINT deals_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis(id)
            )
        """)
        
        colnames = ['id', 'municipi_id', 'contacte_id', 'titol', 'etapa', 'valor_setup', 'valor_llicencia', 'prioritat', 'notes_humanes', 'proper_pas', 'data_seguiment', 'data_tancament_prev', 'data_tancament_real', 'motiu_perdua', 'created_at', 'updated_at']
        
        print(f"📥 Injectant {len(data)} deals...")
        for row in data:
            # Neteja de camps buits
            for c in colnames:
                val = row.get(c)
                if val == '' or val is None:
                    row[c] = None
                elif isinstance(val, str):
                    row[c] = val.strip()

            values = [row.get(c) for c in colnames]
            placeholders = ", ".join(["%s"] * len(colnames))
            cur.execute(f"INSERT INTO public.deals ({', '.join([f'\"{c}\"' for c in colnames])}) VALUES ({placeholders})", values)
        
        conn.commit()
        print("✨ FRESH START DEALS COMPLETAT AMB ÈXIT!")
        
        cur.execute("SELECT COUNT(*) FROM public.deals")
        print(f"📊 Registres totals ara: {cur.fetchone()[0]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    fresh_start_deals()
