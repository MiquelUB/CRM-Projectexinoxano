
import os
import sys
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add current path to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from database import Base, SessionLocal
import models
import models_v2
from services.agent_kimi_k2 import AgentKimiK2

def test_connection():
    load_dotenv()
    db = SessionLocal()
    try:
        print("--- TEST AGENT CONNECTION ---")
        agent = AgentKimiK2(db)
        
        # Test basic query
        count = db.query(models_v2.MunicipiLifecycle).count()
        print(f"Municipis V2: {count}")
        
        # Test fallback logic B-01
        # Busquem un ID que existeixi a V1 (municipis)
        municipi_v1 = db.query(models.Municipi).first()
        if municipi_v1:
            print(f"Provant fallback per {municipi_v1.nom} (ID: {municipi_v1.id})")
            # Simulem crida al xat
            # No podem fer la cridada real a l'IA sense API KEY, però testegem el load_context
            activitats = agent._load_context(municipi_v1.id)
            print(f"Context carregat: {len(activitats)} activitats.")
        else:
            print("No s'han trobat municipis V1 per testejar fallback.")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
