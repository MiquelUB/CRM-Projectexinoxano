from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime, timedelta
# Import schemas only if needed, for simplicity we return counts or raw dicts

router = APIRouter(prefix="/alertes", tags=["Alertes"])

@router.get("/count")
def get_alertes_count(db: Session = Depends(get_db)):
    from models_v2 import TascaV2, EmailV2
    from models import Llicencia, Pagament
    
    tasques_urgents = db.query(TascaV2).filter(TascaV2.prioritat == "alta", TascaV2.estat == "pendent").count()
    emails_pendents = db.query(EmailV2).filter(EmailV2.municipi_id == None).count()
    vencuts = db.query(Pagament).filter(Pagament.estat == "vencut").count()
    
    target_date = datetime.now().date() + timedelta(days=30)
    renovacions = db.query(Llicencia).filter(
        Llicencia.data_renovacio <= target_date,
        Llicencia.estat == "activa"
    ).count()
    
    total = tasques_urgents + emails_pendents + vencuts + renovacions
    
    return {
        "total": total,
        "renovacions": renovacions,
        "vencuts": vencuts,
        "emails_pendents": emails_pendents,
        "tasques_urgents": tasques_urgents
    }

@router.get("/")
def get_alertes(db: Session = Depends(get_db)):
    try:
        from models_v2 import TascaV2, EmailV2, MunicipiLifecycle
        from models import Llicencia, Pagament
        
        # 1. Tasques Urgents
        tasques_v2 = db.query(TascaV2).filter(TascaV2.prioritat == "alta", TascaV2.estat == "pendent").all()
        
        # 2. Emails Pendents
        emails_pendents = db.query(EmailV2).filter(EmailV2.municipi_id == None).limit(50).all()
        
        # 3. Renovacions
        target_date = datetime.now().date() + timedelta(days=30)
        renovacions_query = db.query(Llicencia).filter(
            Llicencia.data_renovacio <= target_date,
            Llicencia.estat == "activa"
        ).all()
        
        # 4. Pagaments Vencuts
        vencuts_query = db.query(Pagament).filter(Pagament.estat == "vencut").all()

        return {
            "renovacions": [
                {
                    "id": str(r.id),
                    "data_renovacio": r.data_renovacio,
                    "municipi_id": str(r.deal.municipi_id) if (r.deal and r.deal.municipi_id) else None,
                    "nom_municipi": r.deal.municipi.nom if (r.deal and r.deal.municipi) else "Municipi desconegut"
                } for r in renovacions_query
            ],
            "pagaments_vencuts": [
                {
                    "id": str(p.id),
                    "import": float(p.import_),
                    "data_limit": p.data_limit,
                    "municipi_id": str(p.llicencia.deal.municipi_id) if (p.llicencia and p.llicencia.deal) else None,
                    "nom_municipi": p.llicencia.deal.municipi.nom if (p.llicencia and p.llicencia.deal and p.llicencia.deal.municipi) else "Municipi desconegut"
                } for p in vencuts_query
            ],
            "tasques_urgents": [
                 {
                    "id": str(t.id),
                    "titol": t.titol,
                    "descripcio": t.descripcio,
                    "data_venciment": t.data_venciment,
                    "tipus": "tasca",
                    "prioritat": t.prioritat,
                    "municipi_id": str(t.municipi_id),
                    "nom_municipi": (t.municipi.nom if t.municipi else "CRM"),
                    "is_pseudo": False
                } for t in tasques_v2
            ],
            "emails_pendents": [
                {
                    "id": str(e.id),
                    "assumpte": e.assumpte,
                    "from": e.from_address,
                    "data": e.data_enviament
                } for e in emails_pendents
            ]
        }
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "status": "error"
        }
