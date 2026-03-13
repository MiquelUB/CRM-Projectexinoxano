from database import SessionLocal
import models
from decimal import Decimal

db = SessionLocal()
d = db.query(models.Deal).filter(models.Deal.valor_setup == Decimal("6000.00")).first()
if d:
    print(f"Fixing deal: {d.titol}")
    d.valor_setup = Decimal("3500.00")
    d.valor_llicencia = Decimal("2500.00")
    d.titol = "ROURE5 - Projecte"
    db.commit()
    print("Fixed.")
else:
    print("No deal with 6000 setup found.")
db.close()
