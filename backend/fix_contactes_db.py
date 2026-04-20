
import os
from sqlalchemy import create_all_metadata, text
from database import engine

def fix_contactes_columns():
    with engine.connect() as conn:
        print("Reparant columnes de la taula contactes...")
        try:
            # 1. Convertir carrec a VARCHAR amb casting explícit (necessari en Postgres per Enums)
            conn.execute(text("ALTER TABLE contactes ALTER COLUMN carrec TYPE VARCHAR(100) USING carrec::text"))
            conn.execute(text("ALTER TABLE contactes ALTER COLUMN carrec SET DEFAULT 'altre'"))
            conn.execute(text("ALTER TABLE contactes ALTER COLUMN carrec DROP NOT NULL"))
            
            # 2. Convertir to_preferit a VARCHAR amb casting explícit
            conn.execute(text("ALTER TABLE contactes ALTER COLUMN to_preferit TYPE VARCHAR(50) USING to_preferit::text"))
            
            # 3. Fix email_sequencies (afegir created_at si falta)
            try:
                conn.execute(text("ALTER TABLE email_sequencies ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()"))
            except Exception as e:
                print(f"Nota: No s'ha pogut afegir created_at: {e}")

            # 4. Neteja de duplicats de municipis
            print("Detectant municipis duplicats...")
            res = conn.execute(text("""
                WITH duplicates AS (
                    SELECT id, nom, 
                           ROW_NUMBER() OVER(PARTITION BY nom ORDER BY data_ultima_accio DESC, created_at DESC) as row_num
                    FROM municipis
                )
                SELECT id, nom FROM duplicates WHERE row_num > 1
            """))
            to_delete = res.fetchall()
            if to_delete:
                print(f"S'han trobat {len(to_delete)} duplicats per eliminar.")
                for d_id, d_nom in to_delete:
                    print(f"Eliminant duplicat: {d_nom} ({d_id})")
                    try:
                        conn.execute(text("DELETE FROM municipis WHERE id = :id"), {"id": d_id})
                    except Exception as delete_err:
                        print(f"No s'ha pogut eliminar {d_nom}: {delete_err}")
            else:
                print("No s'han trobat duplicats.")

            conn.commit()
            print("✅ Taules i dades reparades amb èxit!")
        except Exception as e:
            print(f"❌ Error reparant taula: {e}")
            conn.rollback()

if __name__ == "__main__":
    fix_contactes_columns()
