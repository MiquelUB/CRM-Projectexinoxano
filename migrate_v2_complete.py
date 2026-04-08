import csv
import psycopg2
import json

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def migrate_v2_complete():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # 1. Carregar dades dels fitxers
        print("📖 Llegint CSVs de la Versió 2...")
        with open("migracio_dades/municipis_lifecycle_rows.csv", 'r', encoding='utf-8') as f:
            lifecycle_data = list(csv.DictReader(f))
        
        with open("migracio_dades/contactes_v2_rows.csv", 'r', encoding='utf-8') as f:
            contactes_v2_data = list(csv.DictReader(f))

        # 2. Buidar taules existents
        print("🔥 Buidant taules V2 per netejar el terreny...")
        cur.execute("TRUNCATE TABLE public.contactes_v2 CASCADE")
        cur.execute("TRUNCATE TABLE public.municipis_lifecycle CASCADE")

        # 3. PAS 1: Inserir municipis_lifecycle (SENSE actor_principal_id per evitar el circular error)
        print("🏗️ Pas 1: Inserint municipis_lifecycle (provisionals)...")
        l_cols = [
            'id', 'nom', 'comarca', 'poblacio', 'geografia', 'diagnostic_digital', 
            'angle_personalitzacio', 'etapa_actual', 'historial_etapes', 
            'blocker_actual', 'temperatura', 'dies_etapa_actual', 'data_conversio', 
            'pla_contractat', 'estat_final', 'data_creacio', 
            'data_ultima_accio', 'usuari_asignat'
        ]
        for row in lifecycle_data:
            clean_row = {}
            for c in l_cols:
                val = row.get(c)
                if val == '' or val is None: clean_row[c] = None
                elif c in ['diagnostic_digital', 'historial_etapes']:
                    clean_row[c] = val if val.strip() else '{}'
                else: clean_row[c] = val.strip() if isinstance(val, str) else val
            
            phs = ", ".join(["%s"] * len(l_cols))
            cur.execute(f"INSERT INTO public.municipis_lifecycle ({', '.join(l_cols)}) VALUES ({phs})", [clean_row.get(c) for c in l_cols])

        # 4. PAS 2: Inserir contactes_v2 (ja podem perquè els municipis existeixen)
        print("🏗️ Pas 2: Inserint contactes_v2...")
        c_cols = ['id', 'municipi_id', 'nom', 'carrec', 'email', 'telefon', 'actiu', 'principal', 'angles_exitosos', 'angles_fallits', 'moment_optimal', 'to_preferit', 'data_creacio']
        for row in contactes_v2_data:
            clean_row = {}
            for c in c_cols:
                val = row.get(c).strip() if row.get(c) else None
                if c == 'actiu' or c == 'principal':
                    clean_row[c] = (val.lower() == 'true') if val else False
                elif c in ['angles_exitosos', 'angles_fallits']:
                    clean_row[c] = val if val else '[]'
                else:
                    clean_row[c] = val
            
            phs = ", ".join(["%s"] * len(c_cols))
            cur.execute(f"INSERT INTO public.contactes_v2 ({', '.join(c_cols)}) VALUES ({phs})", [clean_row.get(c) for c in c_cols])

        # 5. PAS 3: Vincular actor_principal_id als municipis
        print("🏗️ Pas 3: Vinculant actors principals als municipis...")
        for row in lifecycle_data:
            m_id = row.get('id')
            actor_id = row.get('actor_principal_id')
            if actor_id and actor_id.strip():
                cur.execute("UPDATE public.municipis_lifecycle SET actor_principal_id = %s WHERE id = %s", (actor_id.strip(), m_id))

        conn.commit()
        print("✨ MIGRACIÓ COMPLETA IA (V2) FINALITZADA AMB ÈXIT!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    migrate_v2_complete()
