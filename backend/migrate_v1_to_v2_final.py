import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
from datetime import datetime

conn_str = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def migrate():
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("Iniciant migració profunda V1 a V2...")
    
    # 1. Obtenir dades V1
    cur.execute("SELECT * FROM municipis")
    v1_municipis = cur.fetchall()
    
    cur.execute("SELECT * FROM contactes")
    v1_contactes = cur.fetchall()
    
    cur.execute("SELECT * FROM deals")
    v1_deals = cur.fetchall()
    
    cur.execute("SELECT * FROM emails")
    v1_emails = cur.fetchall()
    
    cur.execute("SELECT * FROM tasques")
    v1_tasques = cur.fetchall()
    
    id_map = {} # v1_id (Int/UUID) -> v2_uuid
    contact_id_map = {}
    
    # 2. Migrar Municipis
    print(f"Migrant {len(v1_municipis)} municipis...")
    for m in v1_municipis:
        cur.execute("SELECT id FROM municipis_lifecycle WHERE nom = %s", (m['nom'],))
        exists = cur.fetchone()
        
        if exists:
            v2_id = str(exists['id'])
        else:
            v2_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO municipis_lifecycle (id, nom, comarca, poblacio, tipus, provincia, codi_postal, web, telefon, adreca, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (v2_id, m['nom'], m['comarca'], str(m['poblacio']), m['tipus'], m['provincia'], m['codi_postal'], m['web'], m['telefon'], m['adreca'], m['created_at']))
        
        id_map[str(m['id'])] = v2_id
        
    # 3. Migrar Contactes
    print(f"Migrant {len(v1_contactes)} contactes...")
    for c in v1_contactes:
        v2_mun_id = id_map.get(str(c['municipi_id']))
        if not v2_mun_id: continue
            
        cur.execute("SELECT id FROM contactes_v2 WHERE email = %s AND municipi_id = %s", (c['email'], v2_mun_id))
        exists = cur.fetchone()
        if exists:
            contact_id_map[str(c['id'])] = str(exists['id'])
            continue
            
        new_c_id = str(uuid.uuid4())
        carrec = c['carrec'] if c['carrec'] in ['alcalde', 'regidor_turisme', 'tecnic', 'cfo', 'regidor_cultura', 'altre'] else 'altre'
        
        cur.execute("""
            INSERT INTO contactes_v2 (id, municipi_id, nom, carrec, email, telefon, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (new_c_id, v2_mun_id, c['nom'], carrec, c['email'], c['telefon'], c['created_at']))
        contact_id_map[str(c['id'])] = new_c_id
        
    # 4. Migrar Emails
    print(f"Migrant {len(v1_emails)} emails...")
    for e in v1_emails:
        # En V1 els emails podien estar lligats a deals o contactes.
        # Busquem el municipi_id a través del deal o el contacte.
        v2_mun_id = None
        if e['deal_id']:
            cur.execute("SELECT municipi_id FROM deals WHERE id = %s", (e['deal_id'],))
            d = cur.fetchone()
            if d: v2_mun_id = id_map.get(str(d['municipi_id']))
            
        if not v2_mun_id and e['contacte_id']:
            cur.execute("SELECT municipi_id FROM contactes WHERE id = %s", (e['contacte_id'],))
            c = cur.fetchone()
            if c: v2_mun_id = id_map.get(str(c['municipi_id']))
            
        if not v2_mun_id: continue
        
        # Check exists
        cur.execute("SELECT id FROM emails_v2 WHERE assumpte = %s AND data_enviament = %s", (e['assumpte'], e['data_email']))
        if cur.fetchone(): continue
        
        cur.execute("""
            INSERT INTO emails_v2 (id, municipi_id, contacte_id, data_enviament, assumpte, cos, direccio, obert, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), v2_mun_id, contact_id_map.get(str(e['contacte_id'])), e['data_email'], e['assumpte'], e['cos'], 'entrada' if e['direccio'] == 'IN' else 'sortida', e['obert'], e['created_at']))

    # 5. Migrar Tasques
    print(f"Migrant {len(v1_tasques)} tasques...")
    for t in v1_tasques:
        v2_mun_id = id_map.get(str(t['municipi_id']))
        if not v2_mun_id: continue
        
        cur.execute("SELECT id FROM tasques_v2 WHERE titol = %s AND municipi_id = %s", (t['titol'], v2_mun_id))
        if cur.fetchone(): continue
        
        cur.execute("""
            INSERT INTO tasques_v2 (id, municipi_id, titol, descripcio, data_venciment, prioritat, estat, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), v2_mun_id, t['titol'], t['descripcio'], t['data_venciment'], t['prioritat'], t['estat'], t['created_at']))

    conn.commit()
    cur.close()
    conn.close()
    print("Migració profunda completada amb èxit!")

if __name__ == "__main__":
    migrate()
