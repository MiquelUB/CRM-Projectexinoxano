from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime, timedelta
# Import schemas only if needed, for simplicity we return counts or raw dicts

router = APIRouter(prefix="/alertes", tags=["Alertes"])

@router.get("/count")
def get_alertes_count(db: Session = Depends(get_db)):
    emails_pendents = db.query(models.Email).filter(models.Email.deal_id.is_(None)).count()
    vencuts = db.query(models.Pagament).filter(models.Pagament.estat == "vencut").count()
    tasques_urgents = db.query(models.Tasca).filter(models.Tasca.prioritat == "alta", models.Tasca.estat == "pendent").count()
    
    target_date = datetime.now().date() + timedelta(days=30)
    renovacions = db.query(models.Llicencia).filter(
        models.Llicencia.data_renovacio <= target_date,
        models.Llicencia.estat == "activa"
    ).count()
    
    total = emails_pendents + vencuts + renovacions + tasques_urgents
    
    return {
        "total": total,
        "renovacions": renovacions,
        "vencuts": vencuts,
        "emails_pendents": emails_pendents,
        "tasques_urgents": tasques_urgents
    }

@router.get("/")
def get_alertes(db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    target_date = datetime.now().date() + timedelta(days=30)
    
    llicencies = db.query(models.Llicencia).options(
        joinedload(models.Llicencia.deal).joinedload(models.Deal.municipi),
        joinedload(models.Llicencia.deal).joinedload(models.Deal.contacte)
    ).filter(
        models.Llicencia.data_renovacio <= target_date,
        models.Llicencia.estat == "activa"
    ).all()
    
    pagaments_vencuts = db.query(models.Pagament).options(
        joinedload(models.Pagament.llicencia).joinedload(models.Llicencia.deal).joinedload(models.Deal.municipi),
        joinedload(models.Pagament.llicencia).joinedload(models.Llicencia.deal).joinedload(models.Deal.contacte)
    ).filter(models.Pagament.estat == "vencut").all()
    
    emails = db.query(models.Email).filter(models.Email.deal_id.is_(None)).all()
    
    tasques_urgents = db.query(models.Tasca).options(
        joinedload(models.Tasca.deal).joinedload(models.Deal.municipi)
    ).filter(models.Tasca.prioritat == "alta", models.Tasca.estat == "pendent").all()
    
    return {
        "renovacions": [
            {
                "id": str(l.id), 
                "deal_id": str(l.deal_id), 
                "data_renovacio": l.data_renovacio,
                "titol_deal": l.deal.titol if l.deal else "Llicència",
                "nom_municipi": l.deal.municipi.nom if l.deal and l.deal.municipi else "Desconegut"
            } for l in llicencies
        ],
        "pagaments_vencuts": [
            {
                "id": str(p.id), 
                "import": float(p.import_), 
                "data_limit": p.data_limit,
                "deal_id": str(p.llicencia.deal_id) if p.llicencia and p.llicencia.deal else None,
                "titol_deal": p.llicencia.deal.titol if p.llicencia and p.llicencia.deal else "Pagament",
                "nom_municipi": p.llicencia.deal.municipi.nom if p.llicencia and p.llicencia.deal and p.llicencia.deal.municipi else "Desconegut"
            } for p in pagaments_vencuts
        ],
        "tasques_urgents": [
            {
                "id": str(t.id),
                "titol": t.titol,
                "descripcio": t.descripcio,
                "data_venciment": t.data_venciment,
                "tipus": t.tipus,
                "prioritat": t.prioritat,
                "deal_id": str(t.deal_id) if t.deal_id else None,
                "nom_municipi": t.deal.municipi.nom if t.deal and t.deal.municipi else "General",
                "is_pseudo": False
            } for t in tasques_urgents
        ],
        "emails_pendents": [{"id": str(e.id), "assumpte": e.assumpte, "from": e.from_address} for e in emails]
    }
