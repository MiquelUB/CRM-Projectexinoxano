from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from database import get_db
from models import Pagament, Llicencia
from schemas import PagamentOut, PagamentCreate, PagamentUpdate, PagamentListResponse, PagamentKpis
import uuid
from datetime import datetime, date

router = APIRouter(prefix="/pagaments", tags=["Pagaments"])

@router.get("/kpis", response_model=PagamentKpis)
def get_pagaments_kpis(db: Session = Depends(get_db)):
    arr_total = db.query(func.sum(Pagament.import_)).filter(
        Pagament.estat == "confirmat", 
        Pagament.tipus == "llicencia_anual"
    ).scalar() or 0.0
    
    pendent = db.query(func.sum(Pagament.import_)).filter(
        Pagament.estat == "emes"
    ).scalar() or 0.0
    
    vencut = db.query(func.sum(Pagament.import_)).filter(
        Pagament.estat == "vencut"
    ).scalar() or 0.0
    
    proper_30 = db.query(func.count(Pagament.id)).filter(
        Pagament.estat == "proper"
    ).scalar() or 0
    
    return {
        "arr_total": float(arr_total),
        "pendent": float(pendent),
        "vencut": float(vencut),
        "proper_30": proper_30
    }

@router.get("/", response_model=PagamentListResponse)
def get_pagaments(llicencia_id: str = None, estat: str = None, page: int = 1, db: Session = Depends(get_db)):
    query = db.query(Pagament)
    
    if llicencia_id:
        query = query.filter(Pagament.llicencia_id == llicencia_id)
        
    if estat:
        query = query.filter(Pagament.estat == estat)
        
    total = query.count()
    limit = 50
    offset = (page - 1) * limit
    
    items = query.order_by(desc(Pagament.data_emisio)).offset(offset).limit(limit).all()
    
    kpis = get_pagaments_kpis(db) if page == 1 else None
    
    return {
        "items": items,
        "total": total,
        "resum": kpis
    }

@router.post("/", response_model=PagamentOut)
def create_pagament(payload: PagamentCreate, db: Session = Depends(get_db)):
    # verify llicencia exists
    llicencia = db.query(Llicencia).filter(Llicencia.id == str(payload.llicencia_id)).first()
    if not llicencia:
        raise HTTPException(status_code=404, detail="Llicencia not found")
        
    pagament = Pagament(
        llicencia_id=payload.llicencia_id,
        import_=payload.import_,
        tipus=payload.tipus,
        data_emisio=payload.data_emisio,
        data_limit=payload.data_limit,
        estat="emes"
    )
    db.add(pagament)
    db.commit()
    db.refresh(pagament)
    return pagament

@router.patch("/{id}/confirmar", response_model=PagamentOut)
def confirmar_pagament(id: str, payload: dict, db: Session = Depends(get_db)):
    pagament = db.query(Pagament).filter(Pagament.id == id).first()
    if not pagament:
        raise HTTPException(status_code=404, detail="Pagament not found")
        
    data_confirmacio_str = payload.get("data_confirmacio")
    data_confirmacio = None
    if data_confirmacio_str:
        if isinstance(data_confirmacio_str, str):
            try:
                data_confirmacio = datetime.strptime(data_confirmacio_str, "%Y-%m-%d").date()
            except:
                data_confirmacio = datetime.now().date()
    else:
        data_confirmacio = datetime.now().date()
        
    notes = payload.get("notes")
        
    pagament.estat = "confirmat"
    pagament.data_confirmacio = data_confirmacio
    if notes:
        pagament.notes = notes
        
    # Auto recalc llicencia renovacio if this is llicencia anual setup fee...
    # Per especs: El sistema calcula la data_renovacio = data_confirmacio + 365 dies
    if pagament.llicencia:
        from datetime import timedelta
        pagament.llicencia.data_renovacio = data_confirmacio + timedelta(days=365)
        
    db.commit()
    db.refresh(pagament)
    return pagament

@router.patch("/{id}", response_model=PagamentOut)
def update_pagament(id: str, payload: PagamentUpdate, db: Session = Depends(get_db)):
    pagament = db.query(Pagament).filter(Pagament.id == id).first()
    if not pagament:
        raise HTTPException(status_code=404, detail="Pagament not found")
        
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pagament, key, value)
        
    db.commit()
    db.refresh(pagament)
    return pagament
