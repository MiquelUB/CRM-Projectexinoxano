from database import SessionLocal
# Import models 
import models # old models
import models_v2 # new models

db = SessionLocal()
try:
    # 1. Trobem municipi
    m_v2 = db.query(models_v2.MunicipiLifecycle).filter(models_v2.MunicipiLifecycle.nom.ilike("%Sort%")).first()
    if m_v2:
        print(f"Municipi V2: {m_v2.nom} ({m_v2.id})")
        
        # Ens fiquem a buscar en l'antic modelo Deal
        deal_old = db.query(models.Deal).filter(models.Deal.municipi_id == str(m_v2.id)).first()
        if deal_old:
             print(f"Deal Antic Trobat: {deal_old.id} - {deal_old.titol}")
             
             emails_old = db.query(models.Email).filter(models.Email.deal_id == deal_old.id).all()
             print(f"Emails Antics Trobat: {len(emails_old)}")
             for e in emails_old:
                  print(f" - {e.data_email}: {e.assumpte}")
             
        else:
             # Buscar per Nom
             deal_old_by_name = db.query(models.Deal).filter(models.Deal.titol.ilike("%Sort%")).first()
             if deal_old_by_name:
                  print(f"Deal Antic Per Nom Trobat: {deal_old_by_name.id}")
                  emails_old2 = db.query(models.Email).filter(models.Email.deal_id == deal_old_by_name.id).all()
                  print(f"Emails Antics Per Nom Trobat: {len(emails_old2)}")
finally:
    db.close()
