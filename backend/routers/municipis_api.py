from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

import models_v2
from services.agent_kimi_k2 import AgentKimiK2

router = APIRouter(tags=["Municipis API V2"])

class DraftEmailRequest(BaseModel):
    contacte_id: Optional[UUID] = None
    tipus: str

class ProgramarTrucadaRequest(BaseModel):
    contacte_id: Optional[UUID] = None
    data_proposada: datetime
    notes: Optional[str] = None

@router.get("/{municipi_id}/timeline")
async def get_timeline(
    municipi_id: UUID,
    limit: int = Query(50, ge=1, le=100),
    tipus: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models_v2.ActivitatsMunicipi).filter(
        models_v2.ActivitatsMunicipi.municipi_id == municipi_id
    )

    if tipus:
        # filter by tipus parameter
        query = query.filter(models_v2.ActivitatsMunicipi.tipus_activitat.in_(tipus))

    activitats = query.order_by(models_v2.ActivitatsMunicipi.data_activitat.desc()).limit(limit).all()

    timeline = []
    for act in activitats:
        metadata = {}
        if act.tipus_activitat.value == "email":
            metadata["obert"] = act.contingut.get("obert", False)
            metadata["num_obertures"] = act.contingut.get("num_obertures", 0)
            metadata["tracking_token"] = act.contingut.get("tracking_token", "")
        elif act.tipus_activitat.value == "trucada":
            metadata["duracio_minuts"] = act.contingut.get("duracio_minuts", 0)
        elif act.tipus_activitat.value == "reunio":
            metadata["tipus_reunio"] = act.contingut.get("tipus", "general")
            metadata["num_assistents"] = act.contingut.get("num_assistents", 1)

        actor = "Sistema"
        if act.contacte_id:
            c = db.query(models_v2.ContacteV2).filter(models_v2.ContacteV2.id == act.contacte_id).first()
            if c:
                actor = c.nom

        timeline.append({
            "id": act.id,
            "tipus_activitat": act.tipus_activitat.value if hasattr(act.tipus_activitat, 'value') else act.tipus_activitat,
            "data_activitat": act.data_activitat,
            "notes_comercial": act.notes_comercial,
            "metadata": metadata,
            "actor": actor
        })

    return timeline

@router.get("/{municipi_id}/recomanacio")
async def get_recomanacio(municipi_id: UUID, db: Session = Depends(get_db)):
    agent = AgentKimiK2(db)
    context = await agent.analitzar_context(municipi_id)
    recomanacio = await agent.recomanar_accio(municipi_id)
    blockers = agent.detectar_blockers(municipi_id)
    
    ultim_contacte = None
    if context.get("ultim_contacte"):
        ultim_contacte = context["ultim_contacte"]["data"] + f" (fa {context.get('dies_silence', 0)} dies)"

    return {
        "recomanacio": recomanacio,
        "blockers": blockers,
        "ultim_contacte": ultim_contacte,
        "sentiment": context.get("sentiment", "neutre")
    }

@router.post("/{municipi_id}/accions/redactar-email")
async def redactar_email(municipi_id: UUID, payload: DraftEmailRequest, db: Session = Depends(get_db)):
    agent = AgentKimiK2(db)
    variants = await agent.redactar_email(municipi_id, payload.contacte_id, payload.tipus)
    return {"variants": variants}

@router.post("/{municipi_id}/accions/programar-trucada")
async def programar_trucada(municipi_id: UUID, payload: ProgramarTrucadaRequest, db: Session = Depends(get_db)):
    nova_activitat = models_v2.ActivitatsMunicipi(
        municipi_id=municipi_id,
        contacte_id=payload.contacte_id,
        tipus_activitat=models_v2.TipusActivitat.trucada,
        data_activitat=datetime.now(),
        notes_comercial=payload.notes,
        contingut={
            "estat": "programada",
            "data_proposada": payload.data_proposada.isoformat()
        }
    )
    db.add(nova_activitat)
    db.commit()
    db.refresh(nova_activitat)
    return {"status": "success", "activitat_id": nova_activitat.id}

@router.post("/{municipi_id}/accions/marcar-pausa")
async def marcar_pausa(municipi_id: UUID, db: Session = Depends(get_db)):
    municipi = db.query(models_v2.MunicipiLifecycle).filter(models_v2.MunicipiLifecycle.id == municipi_id).first()
    if not municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    municipi.etapa_actual = models_v2.EtapaFunnelEnum.pausa
    
    nova_activitat = models_v2.ActivitatsMunicipi(
        municipi_id=municipi_id,
        tipus_activitat=models_v2.TipusActivitat.canvi_etapa,
        data_activitat=datetime.now(),
        notes_comercial="Marcat en pausa per l'usuari"
    )
    db.add(nova_activitat)
    db.commit()
    return {"status": "success", "message": "Municipi marcat en pausa"}
