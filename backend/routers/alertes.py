from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime, timedelta
# Import schemas only if needed, for simplicity we return counts or raw dicts

router = APIRouter(prefix="/alertes", tags=["Alertes"])

@router.get("/count")
def get_alertes_count(db: Session = Depends(get_db)):
    from models_v2 import TascaV2
    # emails_pendents = db.query(models.Email).filter(models.Email.deal_id.is_(None)).count()
    # vencuts = db.query(models.Pagament).filter(models.Pagament.estat == "vencut").count()
    
    tasques_urgents = db.query(TascaV2).filter(TascaV2.prioritat == "alta", TascaV2.estat == "pendent").count()
    
    # target_date = datetime.now().date() + timedelta(days=30)
    # renovacions = db.query(models.Llicencia).filter(
    #     models.Llicencia.data_renovacio <= target_date,
    #     models.Llicencia.estat == "activa"
    # ).count()
    
    total = tasques_urgents
    
    return {
        "total": total,
        "renovacions": 0,
        "vencuts": 0,
        "emails_pendents": 0,
        "tasques_urgents": tasques_urgents
    }

@router.get("/")
def get_alertes(db: Session = Depends(get_db)):
    try:
        from models_v2 import TascaV2
        tasques_v2 = db.query(TascaV2).filter(TascaV2.prioritat == "alta", TascaV2.estat == "pendent").all()
        
        return {
            "renovacions": [],
            "pagaments_vencuts": [],
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
            "emails_pendents": []
        }
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "status": "error"
        }
