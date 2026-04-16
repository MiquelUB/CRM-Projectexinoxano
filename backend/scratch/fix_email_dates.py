
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    print("Verificant dates de correus...")
    # Netejar dates null
    res = session.execute(text("UPDATE emails SET data_enviament = NOW() WHERE data_enviament IS NULL"))
    print(f"Correus actualitzats amb data fallback: {res.rowcount}")
    
    # Veure els primers correus
    emails = session.execute(text("SELECT id, assumpte, data_enviament FROM emails ORDER BY data_enviament DESC LIMIT 10")).fetchall()
    for e in emails:
        print(f"ID: {e[0]} | Data: {e[2]} | Assumpte: {e[1]}")
    
    session.commit()
except Exception as e:
    print(f"Error: {e}")
    session.rollback()
finally:
    session.close()
