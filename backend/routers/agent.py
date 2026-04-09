from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

from database import get_db
import models
import schemas
from auth import get_current_user
from services.agent_kimi_k2 import AgentKimiK2

@router.post("/redactar-email", response_model=schemas.AgentRedactarEmailResponse)
async def redactar_email(
    request: schemas.AgentRedactarEmailRequest,
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    try:
        agent = AgentKimiK2(db)
        # Nota: El model ara es pot passar opcionalment
        variants = await agent.redactar_email(
            municipi_id=request.municipi_id if hasattr(request, 'municipi_id') else request.deal_id, # Fallback
            contacte_id=request.contacte_id,
            tipus=request.instruccions # O un map de situacions
        )
        # Adaptar format response V1
        if variants:
            v = variants[0]
            return {
                "assumpte": v.get("subject", ""),
                "cos_text": v.get("cos", ""),
                "model_usat": "AgentKimiK2 (variants)",
                "tokens_usats": 0
            }
        return {"assumpte": "", "cos_text": "", "model_usat": "Error"}
    except Exception as e:
        logger.error(f"Error redactar-email: {e}")
        raise HTTPException(status_code=500, detail=f"Error d'IA: {str(e)}")

@router.post("/chat")
async def agent_chat(
    payload: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    try:
        agent = AgentKimiK2(db)
        res = await agent.xat(
            usuari_id=current_user.id,
            message=payload.message,
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
