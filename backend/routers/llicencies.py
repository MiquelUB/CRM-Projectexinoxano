from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import get_db
from models import Llicencia, Deal
from schemas import LlicenciaOut, LlicenciaCreate, LlicenciaUpdate, LlicenciaListResponse
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/llicencies", tags=["Llicencies"])

@router.get("/", response_model=LlicenciaListResponse)
def get_llicencies(deal_id: str = None, estat: str = None, renovacio_propera: int = None, db: Session = Depends(get_db)):
    query = db.query(Llicencia)
    
    if deal_id:
        query = query.filter(Llicencia.deal_id == deal_id)
    
    if estat:
        query = query.filter(Llicencia.estat == estat)
        
    if renovacio_propera is not None:
        target_date = datetime.now().date() + timedelta(days=renovacio_propera)
        query = query.filter(Llicencia.data_renovacio <= target_date, Llicencia.estat == "activa")
        
    items = query.order_by(desc(Llicencia.data_renovacio)).all()
    
    return {"items": items, "total": len(items)}

@router.get("/{id}", response_model=LlicenciaOut)
def get_llicencia(id: str, db: Session = Depends(get_db)):
    llicencia = db.query(Llicencia).filter(Llicencia.id == id).first()
    if not llicencia:
        raise HTTPException(status_code=404, detail="Llicencia not found")
    return llicencia

@router.post("/", response_model=LlicenciaOut)
def create_llicencia(payload: LlicenciaCreate, db: Session = Depends(get_db)):
    # Check if deal exists and is tancat_guanyat
    deal = db.query(Deal).filter(Deal.id == payload.deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
        
    # Check if llicencia already exists for deal
    existing = db.query(Llicencia).filter(Llicencia.deal_id == payload.deal_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Llicencia ja existeix per aquest deal")
        
    llicencia = Llicencia(**payload.dict())
    db.add(llicencia)
    db.commit()
    db.refresh(llicencia)
    return llicencia

@router.patch("/{id}", response_model=LlicenciaOut)
def update_llicencia(id: str, payload: LlicenciaUpdate, db: Session = Depends(get_db)):
    llicencia = db.query(Llicencia).filter(Llicencia.id == id).first()
    if not llicencia:
        raise HTTPException(status_code=404, detail="Llicencia not found")
        
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(llicencia, key, value)
        
    db.commit()
    db.refresh(llicencia)
    return llicencia
