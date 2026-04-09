import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
import models
import models_v2

db = SessionLocal()

try:
    # V1 Totals
    n_municipis_v1 = db.query(models.Municipi).count()
    n_contactes_v1 = db.query(models.Contacte).count()
    n_deals_v1 = db.query(models.Deal).count()
    n_emails_v1 = db.query(models.Email).count()

    # V2 Totals (Actualment)
    n_municipis_v2 = db.query(models_v2.MunicipiLifecycle).count()
    n_contactes_v2 = db.query(models_v2.ContacteV2).count()
    n_emails_v2 = db.query(models_v2.EmailV2).count()
    n_activitats_v2 = db.query(models_v2.ActivitatsMunicipi).count()

    inventory = f"""INVENTARI PRE-MIGRACIÓ (FASE 1.1)
Data: {models_v2.func.now()}

MÓN V1:
- Municipis: {n_municipis_v1}
- Contactes: {n_contactes_v1}
- Deals: {n_deals_v1}
- Emails: {n_emails_v1}

MÓN V2 (ESTAT ACTUAL):
- Municipis Lifecycle: {n_municipis_v2}
- Contactes V2: {n_contactes_v2}
- Emails V2: {n_emails_v2}
- Activitats Municipi: {n_activitats_v2}
"""
    print(inventory)
    with open("inventari_pre_migracio.txt", "w", encoding="utf-8") as f:
        f.write(inventory)

finally:
    db.close()
