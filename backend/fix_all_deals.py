from database import SessionLocal
import models
from decimal import Decimal

db = SessionLocal()
deals = db.query(models.Deal).all()
for d in deals:
    print(f"Checking deal '{d.titol}' (Setup: {d.valor_setup}, Llicencia: {d.valor_llicencia})")
    if d.valor_setup == Decimal("6000.00") and d.valor_llicencia == Decimal("3500.00"):
        print(f"!!! FIXING DEAL '{d.titol}' !!!")
        d.valor_setup = Decimal("3500.00")
        d.valor_llicencia = Decimal("2500.00")
        d.titol = "ROURE (5 rutas)"
db.commit()
db.close()
