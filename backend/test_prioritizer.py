import sys
import os
sys.path.append(os.getcwd())
from database import SessionLocal
from services.prioritizer import get_daily_actions

db = SessionLocal()
try:
    actions = get_daily_actions(db)
    print(f"TOTAL ACTIONS: {len(actions)}")
    for a in actions:
        print(f"[{a.tipus_accio}] {a.nom} -> Score {a.score} | {a.accio_recomanada}")
except Exception as e:
    print("ERROR RUNNING PRIORITIZER:")
    import traceback
    traceback.print_exc()
finally:
    db.close()
