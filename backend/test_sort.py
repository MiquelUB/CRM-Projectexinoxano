import sys
from database import SessionLocal
from models_v2 import MunicipiLifecycle, EmailV2, TrucadaV2

db = SessionLocal()
try:
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.nom.ilike("%Sort%")).first()
    if not m:
        print("Municipi no trobat.")
        sys.exit(0)
        
    print(f"MUNICIPI: {m.nom} ({m.id})")
    
    recent_emails = db.query(EmailV2).filter(EmailV2.municipi_id == m.id).all()
    print(f"Emails found: {len(recent_emails)}")
    for e in recent_emails:
        print(f" - {e.data_enviament}: {e.assumpte}")
        
    recent_calls = db.query(TrucadaV2).filter(TrucadaV2.municipi_id == m.id).all()
    print(f"Calls found: {len(recent_calls)}")
    for c in recent_calls:
        print(f" - {c.data}: {c.notes_breus}")
finally:
    db.close()
