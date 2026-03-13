from database import SessionLocal
import models

db = SessionLocal()
deals = db.query(models.Deal).all()
print(f"Total deals: {len(deals)}")
for d in deals:
    print(f"ID: {d.id} | Titol: {d.titol} | Setup: {d.valor_setup} | Llicencia: {d.valor_llicencia}")
db.close()
