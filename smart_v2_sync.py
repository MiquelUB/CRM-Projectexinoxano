import psycopg2
from psycopg2.extras import execute_values
import uuid

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

ETAPA_MAP = {
    'prospecte': 'contacte',
    'proposta_enviada': 'oferta',
    'negociacio': 'oferta',
    'guanyat': 'client',
    'perdut': 'perdut',
    'reunio_pendent': 'demo_pendent',
    'reunio_feta': 'demo_ok'
}

def sync_v1_to_v2():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("--- Buidant taules V2 per a sincronitzacio neta... ---")
        cur.execute("DELETE FROM public.emails_v2")
        cur.execute("DELETE FROM public.email_drafts_v2")
        cur.execute("DELETE FROM public.activitats_municipi")
        cur.execute("DELETE FROM public.contactes_v2")
        cur.execute("DELETE FROM public.municipis_lifecycle")
        
        # 1. Obtenir dades de Deals V1 fusionades amb Municipis V1
        print("--- Llegint dades de la V1... ---")
        cur.execute("""
            SELECT 
                d.id, m.nom, m.provincia, m.poblacio, d.etapa, 
                d.valor_setup, d.valor_llicencia, d.prioritat, 
                d.notes_humanes, d.proper_pas, d.data_seguiment,
                d.contacte_id, m.provincia
            FROM public.deals d
            JOIN public.municipis m ON d.municipi_id = m.id
        """)
        deals_v1 = cur.fetchall()
        
        print(f"--- Migrant {len(deals_v1)} deals a municipis_lifecycle (V2)... ---")
        
        for d in deals_v1:
            d_id, d_nom, d_prov_1, d_poblacio, d_etapa, d_setup, d_llic, d_prio, d_notes, d_pas, d_seg, d_cont_id, d_prov_ref = d
            
            # Map etapa
            etapa_v2 = ETAPA_MAP.get(d_etapa, 'research')
            
            # Insert V2 (comarca = provincia per ara)
            cur.execute("""
                INSERT INTO public.municipis_lifecycle (
                    id, nom, comarca, poblacio, etapa_actual, 
                    valor_setup, valor_llicencia, prioritat, 
                    notes_humanes, proper_pas, data_seguiment,
                    diagnostic_digital, historial_etapes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                d_id, d_nom, d_prov_1, d_poblacio, etapa_v2,
                d_setup, d_llic, d_prio or 'mitjana',
                d_notes, d_pas, d_seg,
                '{}', '[]'
            ))
            
        print("--- Migrant contactes a la V2... ---")
        cur.execute("""
            SELECT id, municipi_id, nom, carrec, email, telefon
            FROM public.contactes
        """)
        contactes_v1 = cur.fetchall()
        for c in contactes_v1:
            c_id, c_m_id, c_nom, c_carrec, c_email, c_telef = c
            
            # Cerca lifecycle pel nom del municipi
            cur.execute("SELECT id FROM public.municipis_lifecycle WHERE nom = (SELECT nom FROM public.municipis WHERE id = %s) LIMIT 1", (c_m_id,))
            lifecycle_res = cur.fetchone()
            if lifecycle_res:
                l_id = lifecycle_res[0]
                cur.execute("""
                    INSERT INTO public.contactes_v2 (
                        id, municipi_id, nom, carrec, email, telefon, actiu, principal
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (c_id, l_id, c_nom, c_carrec or 'altre', c_email, c_telef, True, False))

        conn.commit()
        print("+++ SINCRONITZACIO V1 -> V2 COMPLETADA AMB EXIT! +++")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"!!! ERROR: {str(e)} !!!")

if __name__ == "__main__":
    sync_v1_to_v2()
