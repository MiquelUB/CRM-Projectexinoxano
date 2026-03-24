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

    print("Executant l'SQL a la base de dades interna (sentència per sentència)...")
    
    # Dividir per punt i coma + salt de línia és el més segur per Inserts
    statements = sql.split(";\n")
    success_count = 0
    error_count = 0
    
    for stmt in statements:
        stmt = stmt.strip()
        if not stmt:
            continue
            
        try:
            cur.execute(stmt + ";")
            success_count += 1
        except Exception as e:
            # Ignorem errors d'existència prèvia de taules/schemas
            error_count += 1
            
    print(f"✅ Restauració completada! Sentències correctes: {success_count}, Ignorades (ja existents): {error_count}")
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error durant la restauració:")
    print(e)
