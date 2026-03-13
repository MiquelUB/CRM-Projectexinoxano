from database import SessionLocal
import models
from sqlalchemy.orm import joinedload

db = SessionLocal()
contactes = db.query(models.Contacte).options(joinedload(models.Contacte.municipi)).all()
print(f"Total contactes: {len(contactes)}")
for c in contactes:
    print(f"Contacte: {c.nom}, Municipi ID: {c.municipi_id}, Municipi Obj: {c.municipi}")
    if c.municipi:
        print(f"  Municipi Nom: {c.municipi.nom}")
db.close()
