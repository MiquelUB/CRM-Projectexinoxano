from database import SessionLocal
import models
import schemas
from uuid import UUID

db = SessionLocal()
m = db.query(models.Municipi).first()
if m:
    print(f"Testing serialization for municipi: {m.nom}")
    try:
        out = schemas.MunicipiDetailOut.model_validate(m)
        print("Serialization success")
    except Exception as e:
        print(f"Serialization failed: {e}")
else:
    print("No municipi found in DB")
db.close()
