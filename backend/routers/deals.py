from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime, timedelta

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/deals", tags=["deals"])

@router.get("/kpis", response_model=schemas.DealKpis)
def get_deals_kpis(db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    # 1. Basic counts - be more inclusive with stages
    # Pipeline is usually everything except closed (won/lost)
    # But for a general "Total Deals" on dashboard, let's include everything except "perdut"
    total_deals = db.query(models.Deal).filter(models.Deal.etapa != "perdut").count()
    
    # 2. Pipeline Value - include all deals not lost
    valor_setup_sum = db.query(func.sum(models.Deal.valor_setup)).filter(models.Deal.etapa != "perdut").scalar() or 0
    valor_llicencia_sum = db.query(func.sum(models.Deal.valor_llicencia)).filter(models.Deal.etapa != "perdut").scalar() or 0
    valor_total = float(valor_setup_sum + valor_llicencia_sum)
    
    # 3. Monthly target (fix SQLite extract issue by using date range)
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    if today.month == 12:
        start_of_next_month = date(today.year + 1, 1, 1)
    else:
        start_of_next_month = date(today.year, today.month + 1, 1)
        
    per_tancar = db.query(models.Deal).filter(
        models.Deal.etapa != "perdut",
        models.Deal.etapa != "tancat_guanyat",
        models.Deal.etapa != "guanyat",
        models.Deal.data_tancament_prev >= start_of_month,
        models.Deal.data_tancament_prev < start_of_next_month
    ).count()
    
    # 4. Inactive deals (14 days)
    data_limit_activitat = datetime.now() - timedelta(days=14)
    sense_activitat = db.query(models.Deal).filter(
        models.Deal.etapa != "perdut",
        models.Deal.etapa != "tancat_guanyat",
        models.Deal.etapa != "guanyat",
        models.Deal.updated_at < data_limit_activitat
    ).count()
    
    return {
        "total_deals": total_deals,
        "valor_total_pipeline": valor_total,
        "deals_per_tancar_aquest_mes": per_tancar,
        "deals_sense_activitat_14_dies": sense_activitat
    }

@router.get("", response_model=schemas.DealListResponse)
def get_deals(
    etapa: Optional[str] = None,
    municipi_id: Optional[UUID] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    query = db.query(models.Deal).options(
        joinedload(models.Deal.municipi),
        joinedload(models.Deal.contacte)
    )
    
    if etapa:
        query = query.filter(models.Deal.etapa == etapa)
    if municipi_id:
        query = query.filter(models.Deal.municipi_id == municipi_id)
        
    total = query.count()
    items = query.order_by(models.Deal.updated_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return {"items": items, "total": total}

@router.get("/{id}", response_model=schemas.DealDetailOut)
def get_deal(id: UUID, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    deal = db.query(models.Deal).options(
        joinedload(models.Deal.municipi),
        joinedload(models.Deal.contacte),
        joinedload(models.Deal.activitats)
    ).filter(models.Deal.id == id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal no trobat")
    
    # Sort activities by date desc for the UI list
    deal.activitats = sorted(deal.activitats, key=lambda x: x.created_at, reverse=True)
    return deal

@router.post("", response_model=schemas.DealShortOut, status_code=status.HTTP_201_CREATED)
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_deal = models.Deal(**deal.model_dump())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal

@router.put("/{id}", response_model=schemas.DealShortOut)
def update_deal(id: UUID, deal: schemas.DealUpdate, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_deal = db.query(models.Deal).filter(models.Deal.id == id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal no trobat")
    
    update_data = deal.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_deal, key, value)
        
    db.commit()
    db.refresh(db_deal)
    return db_deal

@router.patch("/{id}/etapa", response_model=schemas.DealShortOut)
def update_deal_etapa(id: UUID, etapa: str = Body(embed=True), db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_deal = db.query(models.Deal).filter(models.Deal.id == id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal no trobat")
    
    valor_anterior = db_deal.etapa
    db_deal.etapa = etapa
    
    # Log activity
    activitat = models.DealActivitat(
        deal_id=id,
        tipus="canvi_etapa",
        descripcio=f"Canvi d'etapa: de '{valor_anterior}' a '{etapa}'",
        valor_anterior=valor_anterior,
        valor_nou=etapa
    )
    db.add(activitat)
    
    db.commit()
    db.refresh(db_deal)
    return db_deal

@router.patch("/{id}/notes", response_model=schemas.DealShortOut)
def update_deal_notes(id: UUID, notes_humanes: str = Body(embed=True), db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_deal = db.query(models.Deal).filter(models.Deal.id == id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal no trobat")
    
    db_deal.notes_humanes = notes_humanes
    
    # Log activity (briefly)
    activitat = models.DealActivitat(
        deal_id=id,
        tipus="nota",
        descripcio=f"Nota afegida: {notes_humanes[:50]}..." if notes_humanes else "Nota buidada"
    )
    db.add(activitat)
    
    db.commit()
    db.refresh(db_deal)
    return db_deal

@router.patch("/{id}/proper-pas", response_model=schemas.DealShortOut)
def update_deal_proper_pas(
    id: UUID, 
    proper_pas: Optional[str] = Body(default=None, embed=True), 
    data_seguiment: Optional[date] = Body(default=None, embed=True),
    db: Session = Depends(get_db), 
    current_user: models.Usuari = Depends(get_current_user)
):
    db_deal = db.query(models.Deal).filter(models.Deal.id == id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal no trobat")
    
    if proper_pas is not None:
        db_deal.proper_pas = proper_pas
        # Log activity
        activitat = models.DealActivitat(
            deal_id=id,
            tipus="nota",
            descripcio=f"Proper pas actualitzat: {proper_pas}"
        )
        db.add(activitat)
        
    if data_seguiment is not None:
        db_deal.data_seguiment = data_seguiment
        
    db.commit()
    db.refresh(db_deal)
    return db_deal

@router.delete("/{id}")
def delete_deal(id: UUID, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_deal = db.query(models.Deal).filter(models.Deal.id == id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal no trobat")
    
    db.delete(db_deal)
    db.commit()
    return {"message": "eliminat"}
