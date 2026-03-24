from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.prioritizer import get_daily_actions
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

class ActionRecommendationResponse(BaseModel):
    municipi_id: str
    nom: str
    score: int
    etapa: str
    accio_recomanada: str
    rao: str
    tipus_accio: str = "altre"
    contacte_sugerit_id: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/diari", response_model=List[ActionRecommendationResponse])
async def get_dashboard_diari(db: Session = Depends(get_db)):
    """
    Retorna les accions recomanades per al dashboard diari, 
    ordenades per prioritat i excloent clients/perduts.
    """
    recommendations = await get_daily_actions(db, limit=15)
    
    # Mapear de la clase ActionRecommendation de prioritizer.py a Pydantic
    return [
         ActionRecommendationResponse(
              municipi_id=r.municipi_id,
              nom=r.nom,
              score=r.score,
              etapa=r.etapa,
              accio_recomanada=r.accio_recomanada,
              rao=r.rao,
              tipus_accio=r.tipus_accio,
              contacte_sugerit_id=r.contacte_sugerit_id
         ) for r in recommendations
    ]
