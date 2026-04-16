
import os
from sqlalchemy import text, inspect
from database import engine

def audit_db():
    print("--- INICI AUDITORIA CRM PXX ---")
    try:
        with engine.connect() as conn:
            # 1. Comprovar taules existents
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Taules trobades: {tables}")
            
            if 'contactes' in tables:
                print("\nAuditant taula 'contactes':")
                columns = inspector.get_columns('contactes')
                for col in columns:
                    print(f" - Columna: {col['name']} | Tipus: {col['type']} | Nullable: {col['nullable']}")
            else:
                print("❌ ERROR: La taula 'contactes' NO EXISTEIX!")

            # 2. Intentar una micro-lectura
            res = conn.execute(text("SELECT COUNT(*) FROM contactes"))
            count = res.scalar()
            print(f"\nTotal contactes actuals: {count}")

    except Exception as e:
        print(f"❌ ERROR CRÍTIC D'AUDITORIA: {e}")

if __name__ == "__main__":
    audit_db()
