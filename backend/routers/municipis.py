
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Municipi, Contacte, EtapaFunnelEnum, TemperaturaEnum, Activitat, TipusActivitat, Email
from schemas import (
    MunicipiOut, 
    MunicipiDetailOut, 
    MunicipiCreate,
    ContacteCreate, 
    ContacteOut, 
    ActivitatOut,
    MunicipiPaginationOut
)
from typing import List
from datetime import datetime, timezone, date, timedelta
from pydantic import BaseModel
from sqlalchemy import func

class UpdateNotesRequest(BaseModel):
    angle_personalitzacio: str

class EtapaUpdate(BaseModel):
    etapa: str

router = APIRouter(prefix="/municipis", tags=["municipis"])

@router.get("/kpis")
def get_municipis_kpis(db: Session = Depends(get_db)):
    """
    Calcula KPIs del Pipeline unificat.
    """
    try:
        # 1. Total de deals actius
        total_deals = db.query(Municipi).filter(
            Municipi.etapa_actual.notin_([EtapaFunnelEnum.perdut, EtapaFunnelEnum.pausa])
        ).count()
        
        # 2. Valor Total del Pipeline
        valor_setup = db.query(func.sum(Municipi.valor_setup)).scalar() or 0
        valor_llicencia = db.query(func.sum(Municipi.valor_llicencia)).scalar() or 0
        valor_total = float(valor_setup + valor_llicencia)
        
        # 3. Seguiment mes actual
        today = date.today()
        start_of_month = datetime(today.year, today.month, 1)
        if today.month == 12:
            start_of_next_month = datetime(today.year + 1, 1, 1)
        else:
            start_of_next_month = datetime(today.year, today.month + 1, 1)
            
        per_tancar = db.query(Municipi).filter(
            Municipi.data_seguiment >= start_of_month,
            Municipi.data_seguiment < start_of_next_month
        ).count()
        
        # 4. Inactive deals (14 days)
        data_limit_activitat = datetime.now() - timedelta(days=14)
        sense_activitat = db.query(Municipi).filter(
            Municipi.etapa_actual.notin_([EtapaFunnelEnum.perdut, EtapaFunnelEnum.pausa, EtapaFunnelEnum.client]),
            Municipi.data_ultima_accio < data_limit_activitat
        ).count()
        
        # 5. Email stats
        total_emails = db.query(Email).count()
        emails_oberts = db.query(Email).filter(Email.obert == True).count()
        taxa = round((emails_oberts / total_emails * 100), 1) if total_emails > 0 else 0
        
        return {
            "total_deals": total_deals,
            "valor_total_pipeline": valor_total,
            "deals_per_tancar_aquest_mes": per_tancar,
            "deals_sense_activitat_14_dies": sense_activitat,
            "total_emails": total_emails,
            "taxa_obertura": taxa
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error calculant KPIs: {str(e)}")

@router.post("/")
def create_municipi(payload: MunicipiCreate, db: Session = Depends(get_db)):
    try:
        new_m = Municipi(**payload.model_dump())
        db.add(new_m)
        db.commit()
        db.refresh(new_m)
        return new_m
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creant municipi: {str(e)}")

@router.get("/", response_model=MunicipiPaginationOut)
def get_municipis(cerca: str = None, limit: int = 50, db: Session = Depends(get_db)):
    try:
        query = db.query(Municipi)
        if cerca:
            query = query.filter(Municipi.nom.ilike(f"%{cerca}%"))
        total = query.count()
        query = query.limit(limit)
        items = query.all()
        return {"items": items, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=MunicipiDetailOut)
def get_municipi_detail(id: str, db: Session = Depends(get_db)):
    m = db.query(Municipi).filter(Municipi.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    return m

@router.get("/{id}/activitats")
def get_municipi_activitats(id: str, db: Session = Depends(get_db)):
    activitats = db.query(Activitat).filter(
        Activitat.municipi_id == id
    ).order_by(Activitat.data_activitat.desc()).limit(50).all()
    
    return [
        {
            "id": str(a.id),
            "tipus": a.tipus_activitat.value if hasattr(a.tipus_activitat, 'value') else a.tipus_activitat,
            "data": a.data_activitat.isoformat() if a.data_activitat else None,
            "notes": a.notes_comercial,
        }
        for a in activitats
    ]

@router.patch("/{id}/etapa")
def canviar_etapa(id: str, payload: EtapaUpdate, db: Session = Depends(get_db)):
    m = db.query(Municipi).filter(Municipi.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    for enum_val in EtapaFunnelEnum:
        if enum_val.value == payload.etapa:
            old_val = m.etapa_actual.value if m.etapa_actual else "unknown"
            m.etapa_actual = enum_val
            
            # Update historial
            historial = list(m.historial_etapes) if m.historial_etapes else []
            historial.append({
                "etapa_anterior": old_val,
                "nova_etapa": payload.etapa,
                "data": datetime.now(timezone.utc).isoformat()
            })
            m.historial_etapes = historial
            
            # Log Activity
            activitat = Activitat(
                municipi_id=m.id,
                tipus_activitat=TipusActivitat.canvi_etapa,
                notes_comercial=f"Canvi d'etapa: de '{old_val}' a '{payload.etapa}'",
                data_activitat=datetime.now(timezone.utc)
            )
            db.add(activitat)
            m.data_ultima_accio = datetime.now(timezone.utc)
            
            db.commit()
            return {"status": "success", "nova_etapa": payload.etapa}
            
    raise HTTPException(status_code=400, detail="Etapa invàlida")

@router.put("/{id}")
def update_municipi(id: str, payload: dict, db: Session = Depends(get_db)):
    m = db.query(Municipi).filter(Municipi.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    old_etapa = m.etapa_actual
    
    for key, value in payload.items():
        if hasattr(m, key):
            setattr(m, key, value)
    
    if 'etapa_actual' in payload and payload['etapa_actual'] != old_etapa.value:
        activitat = Activitat(
            municipi_id=m.id,
            tipus_activitat=TipusActivitat.canvi_etapa,
            notes_comercial=f"Canvi d'etapa (Edició): de '{old_etapa.value}' a '{payload['etapa_actual']}'",
            data_activitat=datetime.now(timezone.utc)
        )
        db.add(activitat)
        m.data_ultima_accio = datetime.now(timezone.utc)
            
    db.commit()
    return m

@router.delete("/{id}")
def delete_municipi(id: str, db: Session = Depends(get_db)):
    m = db.query(Municipi).filter(Municipi.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    db.delete(m)
    db.commit()
    return {"status": "success"}
