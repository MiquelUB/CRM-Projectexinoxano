
import os
import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager
import sqlalchemy as sa
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Ensure we can import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from database import SessionLocal, engine
import models
import models_v2

def test_startup_logic():
    print("TEST: Provant l'estat de la DB per al startup...")
    db = SessionLocal()
    try:
        # 1. Comprovar taula usuaris
        print("Checking 'usuaris' table...")
        u_count = db.query(models.Usuari).count()
        print(f"OK: {u_count} usuaris trobats.")
        
        # 2. Comprovar Municipis V2
        print("Checking 'municipis_lifecycle' table...")
        m_count = db.query(models_v2.MunicipiLifecycle).count()
        print(f"OK: {m_count} municipis trobats.")
        
        # 3. Comprovar Memoria Municipis
        print("Checking 'memoria_municipis' table columns...")
        m_mem = db.query(models_v2.MemoriaMunicipi).first()
        if m_mem:
            print(f"OK: Resum tactic trobat: {m_mem.resum_tactic[:50] if m_mem.resum_tactic else 'None'}")
        else:
            print("OK: Taula buida però sense error.")

        # 4. Comprovar dades de l'admin (com a main.py)
        print("Checking admin user...")
        admin = db.query(models.Usuari).filter(models.Usuari.email == "admin@projectexinoxano.cat").first()
        print(f"OK: Admin trobat? {admin is not None}")

        print("\nSUCCESS: El startup logic sembla correcte!")
    except Exception as e:
        print(f"FAIL: Error detectat: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_startup_logic()
