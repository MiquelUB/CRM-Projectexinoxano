import os
import psycopg2

# Carregar la URL de connexió d'Easypanel
db_url = os.getenv("DATABASE_URL")
file_path = "copia_supabase_v4.sql"

if not db_url:
    print("❌ Error: No s'ha trobat la variable DATABASE_URL d'Easypanel.")
    exit(1)

print("--- INICIANT RESTAURACIÓ INTERNA ---")
print(f"Llegint l'arxiu {file_path}...")

try:
    # Connectar a la base de dades utilitzant la cadena de connexió
    conn = psycopg2.connect(db_url)
    conn.autocommit = True  # Permet canviar d'esquema o crear taules sense bloquejos de transacció
    cur = conn.cursor()
    
    with open(file_path, "r", encoding="utf-8") as f:
        # Filtrar comandos de psql que comencen amb \ (especialment al principi de la línia)
        sql = "".join([line for line in f if not line.strip().startswith("\\")])
    
    print("Executant l'SQL a la base de dades interna...")
    cur.execute(sql)
    
    print("✅ Base de dades restaurada amb èxit!")
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error durant la restauració:")
    print(e)
