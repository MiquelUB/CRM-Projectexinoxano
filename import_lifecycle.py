import csv
import psycopg2
from io import StringIO
import json

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"
FILE_PATH = "migracio_dades/municipis_lifecycle_rows.csv"

def import_lifecycle():
    try:
        print(f"📖 Llegint {FILE_PATH}...")
        data = []
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        print(f"👀 Files detectades: {len(data)}")
        
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Com que és Fresh Start, buidem primer (CASCADE per les FKs)
        print("🔥 Buidant taula municipis_lifecycle...")
        cur.execute("TRUNCATE TABLE public.municipis_lifecycle CASCADE")
        
        colnames = [
            'id', 'nom', 'comarca', 'poblacio', 'geografia', 'diagnostic_digital', 
            'angle_personalitzacio', 'etapa_actual', 'historial_etapes', 
            'blocker_actual', 'temperatura', 'dies_etapa_actual', 'data_conversio', 
            'pla_contractat', 'estat_final', 'actor_principal_id', 'data_creacio', 
            'data_ultima_accio', 'usuari_asignat'
        ]
        
        print(f"📥 Injectant {len(data)} municipis amb context IA...")
        for row in data:
            # Netegem nuls i JSONs
            clean_row = {}
            for c in colnames:
                val = row.get(c)
                if val == '' or val is None:
                    clean_row[c] = None
                elif c in ['diagnostic_digital', 'historial_etapes']:
                    # Assegurem que el JSON estigui ben formatat
                    try:
                        if isinstance(val, str):
                            json.loads(val) # Test validity
                            clean_row[c] = val
                        else:
                            clean_row[c] = json.dumps(val)
                    except:
                        clean_row[c] = '{}' if c == 'diagnostic_digital' else '[]'
                else:
                    clean_row[c] = val.strip() if isinstance(val, str) else val

            values = [clean_row.get(c) for c in colnames]
            placeholders = ", ".join(["%s"] * len(colnames))
            cur.execute(f"INSERT INTO public.municipis_lifecycle ({', '.join(colnames)}) VALUES ({placeholders})", values)
        
        conn.commit()
        print("✨ IMPORTACIÓ DE MUNICIPIS_LIFECYCLE COMPLETADA!")
        
        cur.execute("SELECT COUNT(*) FROM public.municipis_lifecycle")
        print(f"📊 Total a la DB: {cur.fetchone()[0]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    import_lifecycle()
