from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
import os

from database import get_db
import models
import schemas
from auth import get_current_user
from services import agent_service
from services.agent_chat_service import AgentChatService

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/redactar-email", response_model=schemas.AgentRedactarEmailResponse)
async def redactar_email(
    request: schemas.AgentRedactarEmailRequest,
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    try:
        res = await agent_service.redactar_email(
            db, 
            request.deal_id, 
            request.instruccions, 
            request.model, 
            request.to_address,
            request.contacte_id
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error d'IA: {str(e)}")

@router.post("/analitzar-deal", response_model=schemas.AgentAnalitzarDealResponse)
async def analitzar_deal(
    request: schemas.AgentAnalitzarDealRequest,
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    try:
        res = await agent_service.analitzar_deal(db, request.deal_id, request.model)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error d'IA: {str(e)}")

@router.post("/resum-deal", response_model=schemas.AgentResumDealResponse)
async def resum_deal(
    request: schemas.AgentResumDealRequest,
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    try:
        res = await agent_service.resumir_deal(db, request.deal_id, request.model)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error d'IA: {str(e)}")

from pydantic import BaseModel
from typing import List, Dict
from models_v2 import MunicipiLifecycle, EmailV2, TrucadaV2

class AgentChatRequest(BaseModel):
    municipi_id: str
    messages: List[Dict[str, str]]

@router.post("/chat_municipi")
async def chat_municipi(
    payload: AgentChatRequest,
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    """
    Chat amb l'Agent d'IA vinculat a un Municipi de manera continuada.
    """
    from services.openrouter_client import call_openrouter

    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == payload.municipi_id).first()
    if not m:
         raise HTTPException(status_code=404, detail="Municipi no trobat")

    notes = m.angle_personalitzacio or "Cap nota registrada encara."
    
    # 1. Carregar darreres interaccions per a donar context actualitzat
    recent_emails = db.query(EmailV2).filter(EmailV2.municipi_id == m.id).order_by(EmailV2.data_enviament.desc()).limit(3).all()
    recent_calls = db.query(TrucadaV2).filter(TrucadaV2.municipi_id == m.id).order_by(TrucadaV2.data.desc()).limit(3).all()

    historic_summary = ""
    for e in reversed(recent_emails): 
         historic_summary += f"- [Email] `{e.assumpte}`: {e.cos[:120].strip()}...\n"
    for c in reversed(recent_calls):
         historic_summary += f"- [Trucada] Notes: {c.notes_breus or 'Sense notes'}\n"

    system_prompt = f"""Ets un expert assessor comercial en vendes B2G (administració pública) a Catalunya. El teu objectiu és ajudar al comercial a guanyar aquest Deal.
Aproximació: Sigues estratègic, resolutiu i dóna consells tàctics (què oferir, quines objeccions poden tenir, arguments de venda).

CONTEXT DEL MUNICIPI ACTUAL:
Nom: {m.nom}
Etapa actual: {m.etapa_actual.value}
Temperatura: {m.temperatura.value}
Anotacions/Angles: {notes}

HISTORIAL RECENT:
{historic_summary if historic_summary else 'Cap interacció recent registrada.'}
"""

    messages = [{"role": "system", "content": system_prompt}] + payload.messages
    
    try:
         ai_res = await call_openrouter(messages)
         return {"role": "assistant", "content": ai_res["content"]}
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Error d'IA: {str(e)}")

class ChatMessageRequest(BaseModel):
    message: str
    deal_id: Optional[UUID] = None
    municipi_id: Optional[UUID] = None
    model: str = "deepseek/deepseek-chat"

@router.post("/chat")
async def agent_chat(
    payload: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    """
    Endpoint principal del xat persistent de l'Agent Kimi K2.
    Gestiona la memòria automàticament a la base de dades.
    """
    try:
        service = AgentChatService(db)
        res = await service.chat(
            usuari_id=current_user.id,
            message=payload.message,
            deal_id=payload.deal_id,
            municipi_id=payload.municipi_id,
            model=payload.model
        )
        return res
    except Exception as e:
        logger.error(f"Error en el xat de l'agent: {e}")
        raise HTTPException(status_code=500, detail=f"Error en el servei de xat: {str(e)}")

@router.get("/memory")
async def get_agent_memory(
    deal_id: Optional[UUID] = None,
    municipi_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    """Retorna l'historial guardat per a un context concret."""
    service = AgentChatService(db)
    memory = await service.get_or_create_memory(current_user.id, deal_id, municipi_id)
    return {
        "history": memory.history,
        "summary": memory.summary
    }

# --- Tracking Pixel (Move prefix to root as /tracking) ---
tracking_router = APIRouter(prefix="/tracking", tags=["tracking"])

@tracking_router.get("/{token}")
async def track_email(token: str, request: Request, db: Session = Depends(get_db)):
    # 1x1 transparent PNG pixel
    pixel = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    email = db.query(models.Email).filter(models.Email.tracking_token == token).first()
    if email:
        # Increment total counter
        email.nombre_obertures += 1
        
        # Only set first open date if not set
        if not email.obert:
            email.obert = True
            email.data_obertura = datetime.now()
        
        email.ip_obertura = request.client.host if request.client else "desconeguda"
        db.commit()
    
    return Response(content=pixel, media_type="image/png")
