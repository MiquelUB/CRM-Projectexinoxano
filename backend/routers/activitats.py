
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from database import get_db
import models
import schemas

router = APIRouter(prefix="/activitats", tags=["Activitats"])

@router.post("/", response_model=schemas.ActivitatOut, status_code=status.HTTP_201_CREATED)
def create_activitat(activitat: schemas.ActivitatCreate, db: Session = Depends(get_db)):
    municipi = db.query(models.Municipi).filter(models.Municipi.id == activitat.municipi_id).first()
    if not municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    db_activitat = models.Activitat(
        municipi_id=activitat.municipi_id,
        contacte_id=activitat.contacte_id,
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

@router.get("/municipi/{municipi_id}", response_model=schemas.ActivitatPaginationOut)
def get_municipi_activitats(
    municipi_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    tipus_activitat: Optional[models.TipusActivitat] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Activitat).filter(models.Activitat.municipi_id == municipi_id)
    
    if tipus_activitat:
        query = query.filter(models.Activitat.tipus_activitat == tipus_activitat)
    
    total = query.count()
    pages = (total + limit - 1) // limit
    
    items = query.order_by(desc(models.Activitat.data_activitat))\
                 .offset((page - 1) * limit)\
                 .limit(limit)\
                 .all()
                 
    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": pages
    }

@router.delete("/{activitat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activitat(activitat_id: UUID, db: Session = Depends(get_db)):
    db_activitat = db.query(models.Activitat).filter(models.Activitat.id == activitat_id).first()
    if not db_activitat:
        raise HTTPException(status_code=404, detail="Activitat no trobada")
    
    db.delete(db_activitat)
    db.commit()
    return None
