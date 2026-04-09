import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
import models_v2
from sqlalchemy import func

db = SessionLocal()

try:
    stats = db.query(
        models_v2.ActivitatsMunicipi.tipus_activitat,
        func.count(models_v2.ActivitatsMunicipi.id)
    ).group_by(models_v2.ActivitatsMunicipi.tipus_activitat).all()

    print("ESTADÍSTIQUES D'ACTIVITATS V2:")
    for tipus, count in stats:
        print(f"- {tipus}: {count}")

finally:
    db.close()
