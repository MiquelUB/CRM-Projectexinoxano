import csv
import psycopg2
from io import StringIO

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"
FILE_PATH = "migracio_dades/emails_rows.csv"

def fresh_start_emails():
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
        
        print("🔥 Esborrant taula emails (CASCADE)...")
        cur.execute("DROP TABLE IF EXISTS public.emails CASCADE")
        
        print("🏗️ Creant taula emails de bell nou...")
        cur.execute("""
            CREATE TABLE public.emails (
              id uuid NOT NULL,
              deal_id uuid,
              contacte_id uuid,
              campanya_id uuid,
              from_address character varying NOT NULL,
              to_address character varying NOT NULL,
              assumpte character varying NOT NULL,
              cos text,
              direccio character varying NOT NULL,
              llegit boolean,
              sincronitzat boolean,
              message_id_extern character varying UNIQUE,
              data_email timestamp with time zone NOT NULL,
              created_at timestamp with time zone DEFAULT now(),
              tracking_token character varying UNIQUE,
              obert boolean,
              data_obertura timestamp with time zone,
              nombre_obertures integer,
              ip_obertura character varying,
              CONSTRAINT emails_pkey PRIMARY KEY (id),
              CONSTRAINT emails_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes(id),
              CONSTRAINT emails_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id)
            )
        """)
        
        colnames = [
            'id', 'deal_id', 'contacte_id', 'campanya_id', 'from_address', 'to_address', 
            'assumpte', 'cos', 'direccio', 'llegit', 'sincronitzat', 'message_id_extern', 
            'data_email', 'created_at', 'tracking_token', 'obert', 'data_obertura', 
            'nombre_obertures', 'ip_obertura'
        ]
        
        print(f"📥 Injectant {len(data)} correus...")
        for row in data:
            # Netegem nuls i booleans
            for c in colnames:
                val = row.get(c)
                if val == '' or val is None:
                    row[c] = None
                elif c in ['llegit', 'sincronitzat', 'obert']:
                    row[c] = str(val).lower() == 'true'
                elif c == 'nombre_obertures':
                    try: row[c] = int(val)
                    except: row[c] = 0
                else:
                    if isinstance(val, str):
                        row[c] = val.strip()

            values = [row.get(c) for c in colnames]
            placeholders = ", ".join(["%s"] * len(colnames))
            cur.execute(f"INSERT INTO public.emails ({', '.join([f'\"{c}\"' for c in colnames])}) VALUES ({placeholders})", values)
        
        conn.commit()
        print("✨ FRESH START EMAILS COMPLETAT AMB ÈXIT!")
        
        cur.execute("SELECT COUNT(*) FROM public.emails")
        print(f"📊 Registres totals ara: {cur.fetchone()[0]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    fresh_start_emails()
