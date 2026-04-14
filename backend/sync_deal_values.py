import psycopg2
from psycopg2.extras import RealDictCursor

conn_str = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def sync_deals():
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT * FROM deals")
    v1_deals = cur.fetchall()
    
    print(f"Sincronitzant {len(v1_deals)} deals...")
    updated_count = 0
    for d in v1_deals:
        cur.execute("SELECT nom FROM municipis WHERE id = %s", (d['municipi_id'],))
        mun = cur.fetchone()
        if not mun: continue
        
        etapa_map = {
            'poc_interes': 'research',
            'interessat': 'contacte',
            'demo': 'demo_pendent',
            'proposta': 'oferta',
            'contracte': 'contracte',
            'guanyat': 'client',
            'perdut': 'perdut'
        }
        v2_etapa = etapa_map.get(d['etapa'], 'research')
        
        # Use TRIM to avoid whitespace issues
        cur.execute("""
            UPDATE municipis_lifecycle 
            SET etapa_actual = %s,
                valor_setup = %s,
                valor_llicencia = %s,
                prioritat = %s,
                proper_pas = %s,
                data_seguiment = %s,
                notes_humanes = %s
            WHERE TRIM(nom) = TRIM(%s)
        """, (v2_etapa, d['valor_setup'], d['valor_llicencia'], d['prioritat'], d['proper_pas'], d['data_seguiment'], d['notes_humanes'], mun['nom']))
        
        if cur.rowcount > 0:
            updated_count += 1
            
    conn.commit()
    
    cur.execute("SELECT sum(COALESCE(valor_setup,0) + COALESCE(valor_llicencia,0)) as total FROM municipis_lifecycle")
    total_v2 = cur.fetchone()['total']
    
    cur.close()
    conn.close()
    print(f"Sincronització de deals completada! {updated_count} files afectades.")
    print(f"Total Pipeline V2: {total_v2} EUR")

if __name__ == "__main__":
    sync_deals()
