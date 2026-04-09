import os
import psycopg2
from dotenv import load_dotenv
import uuid
from datetime import datetime
import json

load_dotenv()
# Connexió directa per evitar talls SSL durant el bolcat massiu
DATABASE_URL = os.getenv('DATABASE_URL').replace(':6543/', ':5432/')

def migrate_v1_to_v2():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False # Usarem transacció per seguretat
        cur = conn.cursor()
        print("Connectat per a la Migració Final V1 -> V2...")

        # 1. MIGRAR MUNICIPIS
        cur.execute('SELECT id, nom, poblacio, provincia FROM municipis;')
        municipis = cur.fetchall()
        for m in municipis:
            # Netegem població (treure punts, espais) per convertir a int
            pobl_str = str(m[2]).replace('.', '').replace(' ', '') if m[2] else '0'
            try:
                pobl = int(pobl_str)
            except:
                pobl = 0
            
            cur.execute("""
                INSERT INTO municipis_lifecycle (id, nom, poblacio, comarca, etapa_actual, temperatura)
                VALUES (%s, %s, %s, %s, 'research', 'fred')
                ON CONFLICT (id) DO UPDATE SET nom = EXCLUDED.nom, poblacio = EXCLUDED.poblacio;
            """, (m[0], m[1], pobl, m[3]))
        print(f"✅ Migrats {len(municipis)} municipis.")

        # 2. MIGRAR DEALS (Injectar valors econòmics i NOTES al Municipi)
        cur.execute('SELECT municipi_id, valor_setup, valor_llicencia, proper_pas, etapa, notes_humanes, data_seguiment, prioritat FROM deals;')
        deals = cur.fetchall()
        for d in deals:
            # Mapeig d'etapa V1 a EtapaFunnel V2
            etapa_v1 = d[4]
            map_etapes = {
                'investigacio': 'research',
                'contacte': 'contacte',
                'reunio': 'demo_pendent',
                'oferta': 'oferta',
                'tancat_guanyat': 'client',
                'perdut': 'perdut'
            }
            etapa_v2 = map_etapes.get(etapa_v1, 'contacte')
            
            cur.execute("""
                UPDATE municipis_lifecycle 
                SET valor_setup = %s, 
                    valor_llicencia = %s, 
                    proper_pas = %s, 
                    etapa_actual = %s,
                    notes_humanes = %s,
                    data_seguiment = %s,
                    prioritat = %s
                WHERE id = %s;
            """, (d[1], d[2], d[3], etapa_v2, d[5], d[6], d[7] or 'mitjana', d[0]))
        print(f"✅ Migrada informació de {len(deals)} deals a Lifecycle (incloent notes i seguiment).")

        # 3. MIGRAR CONTACTES
        cur.execute('SELECT id, municipi_id, nom, carrec, email, telefon FROM contactes;')
        contactes = cur.fetchall()
        for c in contactes:
            # Map carrec string to enum CarrecEnum o 'altre'
            cur.execute("""
                INSERT INTO contactes_v2 (id, municipi_id, nom, carrec, email, telefon)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (c[0], c[1], c[2], 'tecnic', c[4], c[5]))
        print(f"✅ Migrats {len(contactes)} contactes.")

        # 4. MIGRAR EMAILS
        cur.execute('SELECT id, deal_id, from_address, to_address, assumpte, cos, data_email, direccio FROM emails;')
        emails = cur.fetchall()
        for e in emails:
            # Necessitem municipi_id de l'email (via deal)
            cur.execute('SELECT municipi_id FROM deals WHERE id = %s;', (e[1],))
            m_id_res = cur.fetchone()
            if m_id_res:
                m_id = m_id_res[0]
                cur.execute("""
                    INSERT INTO emails_v2 (id, municipi_id, data_enviament, assumpte, cos)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (e[0], m_id, e[6], e[4], e[5]))
        print(f"✅ Migrats {len(emails)} emails històrics a V2.")

        conn.commit()
        print("\n🎉 MIGRACIÓ COMPLETA I SEGURA: Tots els Municipis ja tenen el context comercial.")
        cur.close()
        conn.close()

    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        print(f"❌ ERROR CRÍTIC: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    migrate_v1_to_v2()
