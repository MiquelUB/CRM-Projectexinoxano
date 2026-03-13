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
