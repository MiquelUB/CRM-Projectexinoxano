import sys
import os
from sqlalchemy import text
from sqlalchemy.orm import Session

# Afegir el directori arrel al path per poder importar database i models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import SessionLocal

def fix_f405_fk():
    """
    Script per resoldre l'error f405 eliminant la clau forana (FK) de usuari_id 
    a la taula agent_memories_v2, permetent el desacoblament físic a la DB.
    """
    db = SessionLocal()
    try:
        print("--- Iniciant correcció de Schema (Error f405) ---")
        
        # 1. Trobar el nom de la constraint de FK que apunta a 'usuaris'
        query_find_fk = text("""
            SELECT constraint_name 
            FROM information_schema.key_column_usage 
            WHERE table_name = 'agent_memories_v2' 
              AND column_name = 'usuari_id'
              AND constraint_name LIKE '%fkey%';
        """)
        
        result = db.execute(query_find_fk).fetchall()
        
        if not result:
            print("[INFO] No s'ha trobat cap FK activa per a 'usuari_id' a agent_memories_v2.")
        else:
            for row in result:
                fk_name = row[0]
                print(f"[ACTION] Eliminant constraint: {fk_name}...")
                
                # 2. Executar el DROP CONSTRAINT
                drop_query = text(f"ALTER TABLE agent_memories_v2 DROP CONSTRAINT IF EXISTS {fk_name};")
                db.execute(drop_query)
                print(f"[OK] Constraint {fk_name} eliminada correctament.")
        
        # 3. Assegurar que la columna existeix i és indexada (però no FK)
        print("[ACTION] Verificant índex de usuari_id...")
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_agent_memories_v2_usuari_id ON agent_memories_v2 (usuari_id);"))
        
        db.commit()
        print("--- Correcció finalitzada amb èxit ---")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] No s'ha pogut corregir l'esquema: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_f405_fk()
