import psycopg2

conn_str = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

try:
    print(f"Intentant connectar a 178.104.83.189...")
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    print("\n✅ Connexió establerta correctament.")
    print("Taules trobades a l'esquema public d'Easypanel:")
    if not tables:
        print(" (No hi ha taules encara)")
    for t in tables:
        print(f"- {t[0]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"\n❌ Error de connexió a Easypanel: {e}")
