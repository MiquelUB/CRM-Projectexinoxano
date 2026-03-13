from database import SessionLocal
import models

db = SessionLocal()
deals = db.query(models.Deal).all()
for d in deals:
    print(f"'{d.titol}'")
db.close()
