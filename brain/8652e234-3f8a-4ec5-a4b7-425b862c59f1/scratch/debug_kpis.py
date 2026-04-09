from sqlalchemy import create_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import sys

# Afegir el directori backend al path perquè trobi els routers i models
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from database import SessionLocal
from models_v2 import MunicipiLifecycle, EtapaFunnelEnum
from sqlalchemy import func

def test_kpis():
    db = SessionLocal()
    try:
        print("Provant query de KPIs...")
        # Lògica del router municipis_v2.py
        total_deals = db.query(MunicipiLifecycle).filter(
            MunicipiLifecycle.etapa_actual.notin_([EtapaFunnelEnum.perdut, EtapaFunnelEnum.pausa])
        ).count()
        print(f"Total deals: {total_deals}")
        
        valor_setup = db.query(func.sum(MunicipiLifecycle.valor_setup)).scalar() or 0
        valor_llicencia = db.query(func.sum(MunicipiLifecycle.valor_llicencia)).scalar() or 0
        print(f"Valor setup: {valor_setup}, Llicencia: {valor_llicencia}")
        
        return True
    except Exception as e:
        import traceback
        print("\n--- ERROR DETECTAT ---")
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_kpis()
