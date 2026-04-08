import csv
import psycopg2
from io import StringIO

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def fresh_start_tasques_activitats():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # --- 1. TASQUES ---
        print("📖 Llegint tasques_rows.csv...")
        tasques_data = []
        with open("migracio_dades/tasques_rows.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasques_data.append(row)

        print("🔥 Esborrant taula tasques...")
        cur.execute("DROP TABLE IF EXISTS public.tasques CASCADE")
        
        print("🏗️ Creant taula tasques...")
        cur.execute("""
            CREATE TABLE public.tasques (
              id uuid NOT NULL,
              deal_id uuid,
              contacte_id uuid,
              municipi_id uuid,
              usuari_id uuid,
              titol character varying NOT NULL,
              descripcio text,
              data_venciment date NOT NULL,
              tipus character varying,
              prioritat character varying,
              estat character varying,
              created_at timestamp with time zone DEFAULT now(),
              updated_at timestamp with time zone DEFAULT now(),
              CONSTRAINT tasques_pkey PRIMARY KEY (id),
              CONSTRAINT tasques_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes(id),
              CONSTRAINT tasques_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id),
              CONSTRAINT tasques_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis(id),
              CONSTRAINT tasques_usuari_id_fkey FOREIGN KEY (usuari_id) REFERENCES public.usuaris(id)
            )
        """)

        t_cols = ['id', 'deal_id', 'contacte_id', 'municipi_id', 'usuari_id', 'titol', 'descripcio', 'data_venciment', 'tipus', 'prioritat', 'estat', 'created_at', 'updated_at']
        for row in tasques_data:
            vals = [row.get(c) if row.get(c) != '' else None for c in t_cols]
            placeholders = ", ".join(["%s"] * len(t_cols))
            cur.execute(f"INSERT INTO public.tasques ({', '.join(t_cols)}) VALUES ({placeholders})", vals)

        # --- 2. DEAL ACTIVITATS ---
        print("📖 Llegint deal_activitats_rows.csv...")
        activitats_data = []
        with open("migracio_dades/deal_activitats_rows.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                activitats_data.append(row)

        print("🔥 Esborrant taula deal_activitats...")
        cur.execute("DROP TABLE IF EXISTS public.deal_activitats CASCADE")
        
        print("🏗️ Creant taula deal_activitats...")
        cur.execute("""
            CREATE TABLE public.deal_activitats (
              id uuid NOT NULL,
              deal_id uuid NOT NULL,
              tipus character varying NOT NULL,
              descripcio text NOT NULL,
              valor_anterior character varying,
              valor_nou character varying,
              created_at timestamp with time zone DEFAULT now(),
              CONSTRAINT deal_activitats_pkey PRIMARY KEY (id),
              CONSTRAINT deal_activitats_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id)
            )
        """)

        a_cols = ['id', 'deal_id', 'tipus', 'descripcio', 'valor_anterior', 'valor_nou', 'created_at']
        for row in activitats_data:
            vals = [row.get(c) if row.get(c) != '' else None for c in a_cols]
            placeholders = ", ".join(["%s"] * len(a_cols))
            cur.execute(f"INSERT INTO public.deal_activitats ({', '.join(a_cols)}) VALUES ({placeholders})", vals)

        # --- 3. LLICENCIES I PAGAMENTS (BUIDES) ---
        print("🏗️ Creant lllicencies (buida)...")
        cur.execute("DROP TABLE IF EXISTS public.llicencies CASCADE")
        cur.execute("""
            CREATE TABLE public.llicencies (
              id uuid NOT NULL,
              deal_id uuid NOT NULL UNIQUE,
              data_inici date NOT NULL,
              data_renovacio date NOT NULL,
              estat character varying,
              notes text,
              created_at timestamp with time zone DEFAULT now(),
              updated_at timestamp with time zone DEFAULT now(),
              CONSTRAINT llicencies_pkey PRIMARY KEY (id),
              CONSTRAINT llicencies_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id)
            )
        """)

        print("🏗️ Creant pagaments (buida)...")
        cur.execute("DROP TABLE IF EXISTS public.pagaments CASCADE")
        cur.execute("""
            CREATE TABLE public.pagaments (
              id uuid NOT NULL,
              llicencia_id uuid NOT NULL,
              import numeric NOT NULL,
              tipus character varying NOT NULL,
              estat character varying,
              data_emisio date NOT NULL,
              data_limit date,
              data_confirmacio date,
              notes text,
              created_at timestamp with time zone DEFAULT now(),
              updated_at timestamp with time zone DEFAULT now(),
              CONSTRAINT pagaments_pkey PRIMARY KEY (id),
              CONSTRAINT pagaments_llicencia_id_fkey FOREIGN KEY (llicencia_id) REFERENCES public.llicencies(id)
            )
        """)

        conn.commit()
        print("✨ MIGRACIÓ DE TASQUES I ACTIVITATS COMPLETADA!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    fresh_start_tasques_activitats()
