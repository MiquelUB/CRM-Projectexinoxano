
import psycopg2
from uuid import uuid4

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def sync_v1_backup_to_unified():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # 1. Obtenir dades de Municipis V1 Backup
        print("Llegint Municipis V1 Backup...")
        cur.execute("SELECT id, nom, poblacio, tipus, provincia FROM public.municipis_v1_backup")
        v1_municipis = cur.fetchall()
        print(f"Encontrats {len(v1_municipis)} municipis al backup.")

        for m_id, nom, poblacio, tipus, provincia in v1_municipis:
            # Comprovar si ja existeix al unificat
            cur.execute("SELECT id FROM public.municipis WHERE id = %s", (m_id,))
            if not cur.fetchone():
                print(f"Restaurat Municipi: {nom} ({m_id})")
                cur.execute("""
                    INSERT INTO public.municipis (id, nom, tipus, poblacio, provincia, created_at, data_ultima_accio)
                    VALUES (%s, %s, %s, %s, %s, now(), now())
                """, (m_id, nom, tipus or 'ajuntament', str(poblacio) if poblacio else '0', provincia or 'Barcelona'))
            
        # 2. Obtenir dades de Deals V1 Backup
        print("Sincronitzant dades de Deals V1 Backup...")
        cur.execute("SELECT municipi_id, titol, etapa, valor_setup, valor_llicencia, prioritat, proper_pas, notes_humanes FROM public.deals_v1_backup")
        v1_deals = cur.fetchall()
        
        for m_id, titol, etapa, v_setup, v_llicencia, prioritat, proper_pas, notes in v1_deals:
            # Mapetjar etapa V1 a V2 (Enum etapa_funnel)
            # V2 Enum: lead, research, contacte, demo_pendent, demo_ok, oferta, documentacio, aprovacio, contracte, client, pausa, perdut
            etapa_mapping = {
                'prospecte': 'research',
                'en_proces': 'contacte',
                'potencial': 'research',
                'contactat': 'contacte',
                'proposta_enviada': 'oferta',
                'proposta': 'oferta',
                'negociacio': 'oferta',
                'guanyat': 'client',
                'perdut': 'perdut',
                'pausa': 'pausa',
                'demo': 'demo_ok'
            }
            v2_etapa = etapa_mapping.get(etapa.lower() if etapa else '', 'research')

            # Actualitzar dades a Municipis (Unified)
            cur.execute("""
                UPDATE public.municipis 
                SET etapa_actual = %s, 
                    valor_setup = %s, 
                    valor_llicencia = %s, 
                    prioritat = %s, 
                    proper_pas = %s, 
                    notes_humanes = %s,
                    data_ultima_accio = now()
                WHERE id = %s
            """, (v2_etapa, v_setup, v_llicencia, prioritat, proper_pas, notes, m_id))

        conn.commit()
        print("SINCRO COMPLETADA AMB ÈXIT.")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    sync_v1_backup_to_unified()
