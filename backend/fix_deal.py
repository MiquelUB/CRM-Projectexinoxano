from database import SessionLocal
import models
from decimal import Decimal

db = SessionLocal()
# Fix Projecte ROURE5
d = db.query(models.Deal).filter(models.Deal.titol.ilike("%ROURE5%")).first()
if d:
    print(f"Fixing deal: {d.titol}")
    d.valor_setup = Decimal("3500.00")
    d.valor_llicencia = Decimal("2500.00")
    db.commit()
    print("Fixed.")
else:
    print("No ROURE5 deal found.")
db.close()
