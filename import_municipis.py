import json
import psycopg2
from psycopg2.extras import execute_values

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"
FILE_PATH = "migracio_dades/minicipis"

def run_import():
    try:
        print(f"📖 Llegint {FILE_PATH}...")
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.endswith('.'): content = content[:-1]
            data = json.loads(content)
        
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        colnames = ['id', 'nom', 'tipus', 'provincia', 'poblacio', 'web', 'telefon', 'adreca', 'notes', 'created_at', 'updated_at', 'codi_postal']
        quoted_cols = [f'"{c}"' for c in colnames]
        
        # Lògica d'UPSERT per evitar errors de claus duplicades
        update_set = ", ".join([f'"{c}" = EXCLUDED."{c}"' for c in colnames if c != 'id'])
        query = f"""
            INSERT INTO public.municipis ({', '.join(quoted_cols)}) 
            VALUES %s 
            ON CONFLICT (id) DO UPDATE SET {update_set}
        """
        
        rows = [[obj.get(c) for c in colnames] for obj in data]
        
        print(f"📥 Injectant {len(rows)} municipis (UPSERT)...")
        execute_values(cur, query, rows)
        
        conn.commit()
        print(f"✅ IMPORTACIÓ FINALITZADA AMB ÈXIT.")
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    run_import()
