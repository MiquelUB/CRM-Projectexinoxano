import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
import models_v2
from sqlalchemy import func, text

db = SessionLocal()

try:
    print("--- VERIFICACIÓ MANUAL DE MIGRACIÓ (FASE 1.2) ---")
    
    # 1. Notes manuals
    notes_count = db.query(models_v2.ActivitatsMunicipi).filter(models_v2.ActivitatsMunicipi.tipus_activitat == models_v2.TipusActivitat.nota_manual).count()
    print(f"1. Activitats 'nota_manual' (notes migrades): {notes_count}")

    # 2. Emails
    emails_count = db.query(models_v2.ActivitatsMunicipi).filter(models_v2.ActivitatsMunicipi.tipus_activitat.like('email%')).count()
    print(f"2. Activitats 'email%' (emails migrats): {emails_count}")

    # 3. Top 10 Municipis per activitat
    print("\n3. Top 10 Municipis amb més activitat:")
    top_10 = db.query(
        models_v2.MunicipiLifecycle.nom,
        func.count(models_v2.ActivitatsMunicipi.id).label('total')
    ).join(models_v2.ActivitatsMunicipi).group_by(models_v2.MunicipiLifecycle.nom).order_by(text('total DESC')).limit(10).all()
    
    for nom, total in top_10:
        print(f"   - {nom}: {total} activitats")

    # 4. Verificació aleatòria d'un municipi (ex: Isona)
    print("\n4. Verificant Timeline d'Isona (com a mostra):")
    isona = db.query(models_v2.MunicipiLifecycle).filter(models_v2.MunicipiLifecycle.nom.like('%Isona%')).first()
    if isona:
        acts = db.query(models_v2.ActivitatsMunicipi).filter(models_v2.ActivitatsMunicipi.municipi_id == isona.id).order_by(models_v2.ActivitatsMunicipi.data_activitat.desc()).all()
        for a in acts:
            print(f"   - [{a.data_activitat.strftime('%Y-%m-%d')}] [{a.tipus_activitat}] {a.notes_comercial or '(sense notes)'}")
    else:
        print("   - No s'ha trobat Isona per a la verificació.")

finally:
    db.close()
