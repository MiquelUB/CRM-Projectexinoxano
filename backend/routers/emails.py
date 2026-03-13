from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import get_db
from models import Email, Deal
from schemas import EmailResponse, EmailCreate, EmailUpdate
import uuid
import math

from services.email_sender import send_email_from_crm
from services.email_sync import sync_all_emails

router = APIRouter(prefix="/emails", tags=["Emails"])

@router.get("/pendents")
def get_emails_pendents(db: Session = Depends(get_db)):
    emails = db.query(Email).filter(Email.deal_id.is_(None)).order_by(desc(Email.data_email)).all()
    return {"items": emails, "total": len(emails)}

@router.post("/sync")
def force_sync_emails(db: Session = Depends(get_db)):
    try:
        sync_all_emails()
        sincronitzats = db.query(Email).filter(Email.sincronitzat == True).count()
        return {"message": "Sync complete", "sincronitzats": sincronitzats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/obertures")
def get_email_stats(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    trenta_dies_enrera = datetime.now() - timedelta(days=30)
    
    total_rebuts = db.query(Email).count()
    
    enviats = db.query(Email).filter(
        Email.direccio == "OUT",
        Email.data_email >= trenta_dies_enrera
    ).count()
    
    oberts = db.query(Email).filter(
        Email.direccio == "OUT",
        Email.obert == True,
        Email.data_email >= trenta_dies_enrera
    ).count()
    
    taxa = (oberts / enviats * 100) if enviats > 0 else 0
    
    return {
        "enviats_30d": enviats,
        "oberts_30d": oberts,
        "taxa_obertura": round(taxa, 1),
        "total_emails": total_rebuts
    }

@router.get("/")
def get_emails(deal_id: str = None, direccio: str = None, llegit: bool = None, page: int = 1, db: Session = Depends(get_db)):
    query = db.query(Email)
    if deal_id:
        query = query.filter(Email.deal_id == deal_id)
    if direccio:
        query = query.filter(Email.direccio == direccio)
    if llegit is not None:
        query = query.filter(Email.llegit == llegit)
        
    total = query.count()
    limit = 50
    offset = (page - 1) * limit
    
    emails = query.order_by(desc(Email.data_email)).offset(offset).limit(limit).all()
    
    return {
        "items": emails,
        "total": total,
        "page": page,
        "total_pages": math.ceil(total / limit)
    }

@router.post("/enviar")
def enviar_email(payload: dict, db: Session = Depends(get_db)): # Simplified payload for quick impl
    to_address = payload.get("to")
    assumpte = payload.get("assumpte")
    cos = payload.get("cos")
    deal_id = payload.get("deal_id")
    contacte_id = payload.get("contacte_id")
    
    if not to_address or not assumpte or not cos:
        raise HTTPException(status_code=400, detail="Missing required fields")
        
    try:
        email_enviat = send_email_from_crm(to_address, assumpte, cos, deal_id, contacte_id)
        return {"message": "S'ha enviat correctament", "email_id": email_enviat.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@router.get("/{id}")
def get_email(id: str, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@router.patch("/{id}/deal")
def assign_deal_to_email(id: str, payload: dict, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
        
    deal_id = payload.get("deal_id")
    if deal_id:
        deal = db.query(Deal).filter(Deal.id == deal_id).first()
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        email.deal_id = deal_id
    else:
        email.deal_id = None
        
    db.commit()
    db.refresh(email)
    return email

@router.patch("/{id}/llegit")
def mark_email_read(id: str, payload: dict, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
        
    llegit = payload.get("llegit")
    if isinstance(llegit, bool):
        email.llegit = llegit
        db.commit()
        db.refresh(email)
        
    return email

@router.delete("/{id}")
def delete_email(id: str, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    try:
        db.delete(email)
        db.commit()
        return {"message": "Email eliminated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
