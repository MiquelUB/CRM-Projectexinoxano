import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
import models_v2

db = SessionLocal()

try:
    print("Netejant taules V2...")
    db.query(models_v2.MunicipiLifecycle).update({models_v2.MunicipiLifecycle.actor_principal_id: None})
    db.query(models_v2.ActivitatsMunicipi).delete()
    db.query(models_v2.EmailV2).delete()
    db.query(models_v2.ContacteV2).delete()
    db.query(models_v2.MemoriaMunicipi).delete()
    db.query(models_v2.MunicipiLifecycle).delete()
    db.commit()
    print("Taules V2 netes.")
finally:
    db.close()
