
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
            
            conn.commit()
            print("✅ Taula contactes reparada amb èxit (Casting manual realitzat)!")
        except Exception as e:
            print(f"❌ Error reparant taula: {e}")
            conn.rollback()

if __name__ == "__main__":
    fix_contactes_columns()
