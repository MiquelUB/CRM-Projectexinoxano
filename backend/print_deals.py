from database import SessionLocal
import models

db = SessionLocal()
deals = db.query(models.Deal).all()
print("DEALS IN DB:")
for d in deals:
    print(f"ID: {d.id} | Tit: {d.titol} | Set: {d.valor_setup} | Lic: {d.valor_llicencia}")
db.close()
