from sqlalchemy import create_engine, inspect, text
import os

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/crm_pxx" # Canviar si cal
if os.getenv("DATABASE_URL"):
    DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def check_and_fix():
    inspector = inspect(engine)
    
    # 1. Check email_sequencies
    cols = [c['name'] for c in inspector.get_columns("email_sequencies")]
    print(f"Columnes email_sequencies: {cols}")
    
    with engine.connect() as conn:
        if 'created_at' not in cols:
            print("Afegint created_at a email_sequencies...")
            conn.execute(text("ALTER TABLE email_sequencies ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()"))
            conn.commit()
            print("Fet!")

        # 2. Cercar duplicats de Municipis
        print("Cercant municipis duplicats...")
        res = conn.execute(text("""
            SELECT nom, COUNT(*) 
            FROM municipis 
            GROUP BY nom 
            HAVING COUNT(*) > 1
        """))
        duplicates = res.fetchall()
        print(f"Municipis duplicats trobats: {len(duplicates)}")
        for d in duplicates:
            print(f" - {d[0]}: {d[1]} vegades")

if __name__ == "__main__":
    check_and_fix()
