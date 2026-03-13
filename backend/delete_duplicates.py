from database import SessionLocal
import models

db = SessionLocal()
deals = db.query(models.Deal).order_by(models.Deal.created_at).all()
seen = set()
for d in deals:
    key = (d.titol, d.municipi_id)
    if key in seen:
        print(f"Deleting duplicate: {d.titol} for municipi {d.municipi_id}")
        db.delete(d)
    else:
        seen.add(key)
db.commit()
db.close()
