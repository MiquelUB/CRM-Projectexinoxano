import psycopg2
import re

conn_str = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"
sql_file = "dades_inserts.sql"

def migrate():
    try:
        print("🚀 Iniciant migració a Easypanel...")
        conn = psycopg2.connect(conn_str)
        conn.autocommit = False
        cur = conn.cursor()

        # 1. Llegir el fitxer SQL
        print(f"📖 Llegint {sql_file}...")
        with open(sql_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Filtrar només inserts de public (usant regex per ser més robust)
        public_inserts = [l.strip() for l in lines if re.search(r"INSERT INTO public\.", l)]
        print(f"✅ S'han trobat {len(public_inserts)} sentències d'inserció per a l'esquema public.")

        if not public_inserts:
            print("❌ No s'han trobat insercions a l'esquema public. Revisa el format del fitxer.")
            return

        # 2. Llista de taules a netejar
        tables_found = []
        for line in public_inserts:
            match = re.search(r"INSERT INTO public\.(\w+)", line)
            if match:
                t = match.group(1)
                if t not in tables_found:
                    tables_found.append(t)
        
        print(f"🧹 Netejant taules existents: {', '.join(tables_found)}")
        for table in reversed(tables_found):
            try:
                cur.execute(f"TRUNCATE TABLE public.{table} RESTART IDENTITY CASCADE;")
            except Exception as e:
                print(f"  ⚠️ Avís netejant {table}: {e}")
                conn.rollback()
                # Tornem a obrir el cursor després del rollback
                cur = conn.cursor()

        # 3. Executar inserts
        print("📥 Injectant dades...")
        errors = 0
        for i, line in enumerate(public_inserts):
            try:
                # Netejar possibles punts i comes sobrants al final si la línia està mal tallada
                stmt = line.strip()
                if not stmt.endswith(';'):
                    stmt += ';'
                cur.execute(stmt)
            except Exception as e:
                print(f"  ❌ Error línia {i}: {e}")
                print(f"  SQL: {line[:150]}...")
                errors += 1
                if errors > 5:
                    print("🛑 Massa errors, aturant...")
                    break

        if errors == 0:
            conn.commit()
            print("\n✨ MIGRACIÓ COMPLETADA AMB ÈXIT!")
        else:
            conn.rollback()
            print(f"\n❌ Migració avortada per {errors} errors.")
        
        # Verificació final
        cur.execute("SELECT COUNT(*) FROM public.municipis")
        print(f"📊 Total municipis a Easypanel: {cur.fetchone()[0]}")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"💥 Error crític durant la migració: {e}")

if __name__ == "__main__":
    migrate()
