import os
import sys
from sqlalchemy import func
from datetime import date, datetime, timedelta

# Add current dir to path
sys.path.append(os.getcwd())

from database import SessionLocal
import models

def debug():
    db = SessionLocal()
    try:
        print("Testing database connection...")
        count = db.query(models.Deal).count()
        print(f"Total deals in DB: {count}")
        
        print("Testing KPI logic...")
        total_deals = db.query(models.Deal).filter(models.Deal.etapa != "perdut").count()
        print(f"Total deals (not perdut): {total_deals}")
        
        valor_setup_sum = db.query(func.sum(models.Deal.valor_setup)).filter(models.Deal.etapa != "perdut").scalar() or 0
        valor_llicencia_sum = db.query(func.sum(models.Deal.valor_llicencia)).filter(models.Deal.etapa != "perdut").scalar() or 0
        valor_total = float(valor_setup_sum + valor_llicencia_sum)
        print(f"Valor total: {valor_total}")
        
        today = date.today()
        start_of_month = date(today.year, today.month, 1)
        if today.month == 12:
            start_of_next_month = date(today.year + 1, 1, 1)
        else:
            start_of_next_month = date(today.year, today.month + 1, 1)
            
        per_tancar = db.query(models.Deal).filter(
            models.Deal.etapa != "perdut",
            models.Deal.etapa != "tancat_guanyat",
            models.Deal.etapa != "guanyat",
            models.Deal.data_tancament_prev >= start_of_month,
            models.Deal.data_tancament_prev < start_of_next_month
        ).count()
        print(f"Per tancar aquest mes: {per_tancar}")
        
        data_limit_activitat = datetime.now() - timedelta(days=14)
        sense_activitat = db.query(models.Deal).filter(
            models.Deal.etapa != "perdut",
            models.Deal.etapa != "tancat_guanyat",
            models.Deal.etapa != "guanyat",
            models.Deal.updated_at < data_limit_activitat
        ).count()
        print(f"Sense activitat: {sense_activitat}")
        
        print("KPIs logic test passed!")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug()
