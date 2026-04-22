from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(tags=["Tracking"])

@router.get("/tracking/{token}")
def track_email_open(token: str, db: Session = Depends(get_db)):
    email = db.query(models.Email).filter(models.Email.tracking_token == token).first()
    if email:
        email.obert = True
        db.commit()
    # Transparent 1x1 GIF
    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x00\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return Response(content=pixel, media_type="image/gif")
