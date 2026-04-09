import os
from sqlalchemy import create_url, create_engine, func
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load prod env
load_dotenv('backend/.env')
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from backend.models_v2 import MunicipiLifecycle, EtapaFunnelEnum

def test_kpi_query():
    db = SessionLocal()
    try:
        print("Testing KPI query...")
        # 1. Total deals
        total_deals = db.query(MunicipiLifecycle).filter(
            MunicipiLifecycle.etapa_actual.notin_([EtapaFunnelEnum.perdut.value, EtapaFunnelEnum.pausa.value])
        ).count()
        print(f"Total deals: {total_deals}")
        
        # 2. Values
        valor_setup = db.query(func.sum(MunicipiLifecycle.valor_setup)).scalar() or 0
        valor_llicencia = db.query(func.sum(MunicipiLifecycle.valor_llicencia)).scalar() or 0
        print(f"Valor Setup: {valor_setup}")
        print(f"Valor Llicencia: {valor_llicencia}")
        
        valor_total = float(valor_setup + valor_llicencia)
        print(f"Valor Total: {valor_total}")
        
    except Exception as e:
        import traceback
        print(f"ERROR: {e}")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_kpi_query()
