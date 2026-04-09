
import os
import sys
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Ensure we can import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from database import SessionLocal, engine
import models_v2 as m2

def find_broken_table():
    db = SessionLocal()
    tables = [
        ("MunicipiLifecycle", m2.MunicipiLifecycle),
        ("ContacteV2", m2.ContacteV2),
        ("EmailV2", m2.EmailV2),
        ("TrucadaV2", m2.TrucadaV2),
        ("ReunioV2", m2.ReunioV2),
        ("EmailDraftV2", m2.EmailDraftV2),
        ("EmailSequenciaV2", m2.EmailSequenciaV2),
        ("MemoriaMunicipi", m2.MemoriaMunicipi),
        ("MemoriaGlobal", m2.MemoriaGlobal),
        ("PatroMunicipi", m2.PatroMunicipi),
        ("ActivitatsMunicipi", m2.ActivitatsMunicipi),
        ("AgentMemoryV2", m2.AgentMemoryV2),
        ("TascaV2", m2.TascaV2)
    ]
    
    print("DIAGNOSIS: Provant cada taula V2 una per una...")
    for name, model in tables:
        try:
            count = db.query(model).count()
            print(f"[OK] {name}: {count} registres.")
        except Exception as e:
            print(f"[FAIL] {name}: {str(e)}")
    
    db.close()

if __name__ == "__main__":
    find_broken_table()
