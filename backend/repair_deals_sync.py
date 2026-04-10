
import psycopg2
from uuid import uuid4

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def sync_v2_to_v1():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # 1. Obtenir tots els municipis de la V2
        print("Llegint Municipis Lifecycle (V2)...")
        cur.execute("SELECT id, nom, poblacio, etapa_actual, valor_setup, valor_llicencia, prioritat, proper_pas, notes_humanes FROM public.municipis_lifecycle")
        v2_municipis = cur.fetchall()
        print(f"Encontrats {len(v2_municipis)} registres a la V2.")

        for m_v2 in v2_municipis:
            m_id, nom, poblacio, etapa, v_setup, v_llicencia, prioritat, proper_pas, notes = m_v2
            
            # A. Comprovar si existeix a Municipis (V1) o crear-lo
            cur.execute("SELECT id FROM public.municipis WHERE id = %s", (m_id,))
            if not cur.fetchone():
                print(f"Creant Municipi V1 per: {nom} ({m_id})")
                cur.execute("""
                    INSERT INTO public.municipis (id, nom, tipus, poblacio, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, now(), now())
                """, (m_id, nom, 'ajuntament', str(poblacio) if poblacio else '0'))
            
            # B. Comprovar si existeix un Deal (V1) per aquest municipi
            cur.execute("SELECT id FROM public.deals WHERE municipi_id = %s", (m_id,))
            deal = cur.fetchone()
            
            # Mapetjar etapa V2 a V1 (etapa V2 sol ser més moderna)
            v1_etapa = etapa if etapa else 'prospecte'
            if v1_etapa == 'research': v1_etapa = 'prospecte'
            if v1_etapa == 'contacte': v1_etapa = 'en_proces'

            if not deal:
                deal_id = str(uuid4())
                print(f"Creant Deal V1 per: {nom} (Etapa: {v1_etapa})")
                cur.execute("""
                    INSERT INTO public.deals (id, municipi_id, titol, etapa, valor_setup, valor_llicencia, prioritat, proper_pas, notes_humanes, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())
                """, (deal_id, str(m_id), f"Projecte {nom}", v1_etapa, v_setup, v_llicencia, prioritat, proper_pas, notes))
            else:
                # Opcional: Actualitzar dades si ja existeix per si han canviat a la V2
                # print(f"🔄 Actualitzant Deal V1 existent per: {nom}")
                cur.execute("""
                    UPDATE public.deals 
                    SET etapa = %s, valor_setup = %s, valor_llicencia = %s, updated_at = now()
                    WHERE municipi_id = %s
                """, (v1_etapa, v_setup, v_llicencia, str(m_id)))

        conn.commit()
        print("REPARACIO I SINCRONITZACIO COMPLETADA.")
        
        cur.execute("SELECT COUNT(*) FROM deals")
        print(f"Deals totals a la BD (V1): {cur.fetchone()[0]}")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    sync_v2_to_v1()
