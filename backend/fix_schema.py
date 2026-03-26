import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://pxx_admin:b86f95465942a859661e@crmpxx_db-crmpxx:5432/crm_pxx?sslmode=disable"
)

def fix_db():
    print("Connecting to DB...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Checking schemas...")
    cur.execute("SELECT schema_name FROM information_schema.schemata;")
    schemas = [row[0] for row in cur.fetchall()]
    print("Schemas existents:", schemas)
    
    if 'public' not in schemas:
        print("Creating public schema...")
        cur.execute("CREATE SCHEMA public;")
        print("Schema public created.")
    
    print("Granting permissions...")
    cur.execute("GRANT ALL ON SCHEMA public TO current_user;")
    cur.execute("GRANT ALL ON SCHEMA public TO public;")
    print("Permissions granted.")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    fix_db()
