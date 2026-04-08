import psycopg2

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def test_single_insert():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Test simple
        print("Intentant inserció simple d'Isona...")
        cur.execute("INSERT INTO public.municipis (id, nom, provincia) VALUES (%s, %s, %s)", 
                    ('117d35c3-b4c5-406d-a8d4-8cb58393bf52', 'Isona', 'Lleida'))
        
        conn.commit()
        print("✅ Inserció exitosa!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_single_insert()
