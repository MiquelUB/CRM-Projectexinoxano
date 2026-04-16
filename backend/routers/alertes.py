
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/alertes", tags=["Alertes"])

@router.get("/count")
def get_alertes_count(db: Session = Depends(get_db)):
    tasques_urgents = db.query(models.Tasca).filter(
        (models.Tasca.prioritat == 3) | (models.Tasca.prioritat == "alta"), 
        models.Tasca.estat == "pendent"
    ).count()
    
    emails_pendents = db.query(models.Email).filter(models.Email.municipi_id == None).count()
    vencuts = db.query(models.Pagament).filter(models.Pagament.estat == "vencut").count()
    
    # We can add more logic here if needed
    total = tasques_urgents + emails_pendents + vencuts
    
    return {
        "total": total,
        "vencuts": vencuts,
        "emails_pendents": emails_pendents,
        "tasques_urgents": tasques_urgents
    }

@router.get("/")
def get_alertes(db: Session = Depends(get_db)):
    try:
        # 1. Tasques Urgents
        tasques_urgents = db.query(models.Tasca).filter(
            (models.Tasca.prioritat == 3) | (models.Tasca.prioritat == "alta"),
            models.Tasca.estat == "pendent"
        ).all()
        
        # 2. Emails Pendents
        emails_pendents = db.query(models.Email).filter(models.Email.municipi_id == None).limit(50).all()
        
        # 3. Pagaments Vencuts
        vencuts = db.query(models.Pagament).filter(models.Pagament.estat == "vencut").all()

        return {
            "pagaments_vencuts": [
                {
                    "id": str(p.id),
                    "import": float(p.import_),
                    "data_limit": p.data_limit if hasattr(p, 'data_limit') else None,
                    "nom_municipi": p.llicencia.municipi.nom if (p.llicencia and p.llicencia.municipi) else "Innominat"
                } for p in vencuts
            ],
            "tasques_urgents": [
                 {
                    "id": str(t.id),
                    "titol": t.titol,
                    "descripcio": t.descripcio,
                    "data_venciment": t.data_venciment,
                    "tipus": "tasca",
                    "municipi_id": str(t.municipi_id),
                    "nom_municipi": (t.municipi.nom if t.municipi else "CRM"),
                } for t in tasques_urgents
            ],
            "emails_pendents": [
                {
                    "id": str(e.id),
                    "assumpte": e.assumpte,
                    "from": e.from_address,
                    "data": e.data_enviament if hasattr(e, 'data_enviament') else e.data_email
                } for e in emails_pendents
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
