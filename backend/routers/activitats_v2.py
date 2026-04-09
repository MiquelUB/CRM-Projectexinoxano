from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from database import get_db
import models_v2
import schemas_v2

router = APIRouter(prefix="/activitats", tags=["Activitats V2"])

@router.post("/", response_model=schemas_v2.ActivitatOut, status_code=status.HTTP_201_CREATED)
def create_activitat(activitat: schemas_v2.ActivitatCreate, db: Session = Depends(get_db)):
    # Validar que el municipi existeix
    municipi = db.query(models_v2.MunicipiLifecycle).filter(models_v2.MunicipiLifecycle.id == activitat.municipi_id).first()
    if not municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    # Crear l'activitat
    db_activitat = models_v2.ActivitatsMunicipi(
        municipi_id=activitat.municipi_id,
        contacte_id=activitat.contacte_id,
        deal_id=activitat.deal_id,
        tipus_activitat=activitat.tipus_activitat,
        data_activitat=activitat.data_activitat or datetime.now(),
        contingut=activitat.contingut,
        notes_comercial=activitat.notes_comercial,
        generat_per_ia=activitat.generat_per_ia,
        etiquetes=activitat.etiquetes
    )
    
    db.add(db_activitat)
    db.commit()
    db.refresh(db_activitat)
    return db_activitat

@router.get("/municipi/{municipi_id}", response_model=schemas_v2.ActivitatPaginationOut)
def get_municipi_activitats(
    municipi_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    tipus_activitat: Optional[models_v2.TipusActivitat] = None,
    data_inici: Optional[datetime] = None,
    data_fi: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models_v2.ActivitatsMunicipi).filter(models_v2.ActivitatsMunicipi.municipi_id == municipi_id)
    
    if tipus_activitat:
        query = query.filter(models_v2.ActivitatsMunicipi.tipus_activitat == tipus_activitat)
    
    if data_inici:
        query = query.filter(models_v2.ActivitatsMunicipi.data_activitat >= data_inici)
    
    if data_fi:
        query = query.filter(models_v2.ActivitatsMunicipi.data_activitat <= data_fi)
        
    total = query.count()
    pages = (total + limit - 1) // limit
    
    items = query.order_by(desc(models_v2.ActivitatsMunicipi.data_activitat))\
                 .offset((page - 1) * limit)\
                 .limit(limit)\
                 .all()
                 
    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": pages
    }

@router.put("/{activitat_id}", response_model=schemas_v2.ActivitatOut)
def update_activitat(activitat_id: UUID, activitat_update: schemas_v2.ActivitatUpdate, db: Session = Depends(get_db)):
    db_activitat = db.query(models_v2.ActivitatsMunicipi).filter(models_v2.ActivitatsMunicipi.id == activitat_id).first()
    if not db_activitat:
        raise HTTPException(status_code=404, detail="Activitat no trobada")
    
    if activitat_update.notes_comercial is not None:
        db_activitat.notes_comercial = activitat_update.notes_comercial
    
    if activitat_update.etiquetes is not None:
        db_activitat.etiquetes = activitat_update.etiquetes
        
    db.commit()
    db.refresh(db_activitat)
    return db_activitat

@router.delete("/{activitat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activitat(activitat_id: UUID, db: Session = Depends(get_db)):
    db_activitat = db.query(models_v2.ActivitatsMunicipi).filter(models_v2.ActivitatsMunicipi.id == activitat_id).first()
    if not db_activitat:
        raise HTTPException(status_code=404, detail="Activitat no trobada")
    
    # Per ara hard delete segons el checklist (soft delete opcional)
    db.delete(db_activitat)
    db.commit()
    return None
