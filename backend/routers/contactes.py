
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/contactes", tags=["contactes"])

@router.get("", response_model=schemas.ContactePaginationOut)
def get_contactes(
    municipi_id: Optional[UUID] = None,
    cerca: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.Contacte)
    
    if municipi_id:
        query = query.filter(models.Contacte.municipi_id == municipi_id)
    if cerca:
        query = query.filter(
            (models.Contacte.nom.ilike(f"%{cerca}%")) | 
            (models.Contacte.email.ilike(f"%{cerca}%"))
        )
        
    total = query.count()
    items = query.order_by(models.Contacte.nom).offset((page - 1) * limit).limit(limit).all()
    
    return {"items": items, "total": total, "page": page}

@router.get("/{id}", response_model=schemas.ContacteOut)
def get_contacte(id: UUID, db: Session = Depends(get_db)):
    contacte = db.query(models.Contacte).filter(models.Contacte.id == id).first()
    if not contacte:
        raise HTTPException(status_code=404, detail="Contacte no trobat")
    return contacte

@router.post("", response_model=schemas.ContacteOut, status_code=status.HTTP_201_CREATED)
def create_contacte(contacte: schemas.ContacteCreate, db: Session = Depends(get_db)):
    db_contacte = models.Contacte(**contacte.model_dump())
    db.add(db_contacte)
    db.commit()
    db.refresh(db_contacte)
    return db_contacte

@router.put("/{id}", response_model=schemas.ContacteOut)
def update_contacte(id: UUID, contacte: schemas.ContacteUpdate, db: Session = Depends(get_db)):
    db_contacte = db.query(models.Contacte).filter(models.Contacte.id == id).first()
    if not db_contacte:
        raise HTTPException(status_code=404, detail="Contacte no trobat")
    
    update_data = contacte.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_contacte, key, value)
        
    db.commit()
    db.refresh(db_contacte)
    return db_contacte

@router.delete("/{id}")
def delete_contacte(id: UUID, db: Session = Depends(get_db)):
    db_contacte = db.query(models.Contacte).filter(models.Contacte.id == id).first()
    if not db_contacte:
        raise HTTPException(status_code=404, detail="Contacte no trobat")
    
    db.delete(db_contacte)
    db.commit()
    return {"message": "eliminat"}
