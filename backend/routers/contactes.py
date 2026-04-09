from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from uuid import UUID

from database import get_db
import models
import models_v2
import schemas
import schemas_v2
from auth import get_current_user

router = APIRouter(prefix="/contactes", tags=["contactes"])

@router.get("", response_model=schemas_v2.ContactePaginationOut)
def get_contactes(
    municipi_id: Optional[UUID] = None,
    cerca: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    # Migrat a V2: ContacteV2
    query = db.query(models_v2.ContacteV2)
    
    if municipi_id:
        query = query.filter(models_v2.ContacteV2.municipi_id == str(municipi_id))
    if cerca:
        query = query.filter(
            (models_v2.ContacteV2.nom.ilike(f"%{cerca}%")) | 
            (models_v2.ContacteV2.email.ilike(f"%{cerca}%"))
        )
        
    total = query.count()
    items = query.order_by(models_v2.ContacteV2.nom).offset((page - 1) * limit).limit(limit).all()
    
    return {"items": items, "total": total, "page": page}

@router.get("/{id}", response_model=schemas_v2.ContacteOut)
def get_contacte(id: UUID, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    # Migrat a V2: ContacteV2
    contacte = db.query(models_v2.ContacteV2).filter(models_v2.ContacteV2.id == id).first()
    if not contacte:
        raise HTTPException(status_code=404, detail="Contacte no trobat (V2)")
    return contacte

@router.post("", response_model=schemas.ContacteShortOut, status_code=status.HTTP_201_CREATED)
def create_contacte(contacte: schemas.ContacteCreate, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_contacte = models.Contacte(**contacte.model_dump())
    db.add(db_contacte)
    db.commit()
    db.refresh(db_contacte)
    return db_contacte

@router.put("/{id}", response_model=schemas.ContacteShortOut)
def update_contacte(id: UUID, contacte: schemas.ContacteUpdate, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
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
def delete_contacte(id: UUID, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_contacte = db.query(models.Contacte).filter(models.Contacte.id == id).first()
    if not db_contacte:
        raise HTTPException(status_code=404, detail="Contacte no trobat")
    
    db.delete(db_contacte)
    db.commit()
    return {"message": "eliminat"}

@router.patch("/{id}/notes", response_model=schemas.ContacteShortOut)
def update_contacte_notes(id: UUID, notes_humanes: str, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_contacte = db.query(models.Contacte).filter(models.Contacte.id == id).first()
    if not db_contacte:
        raise HTTPException(status_code=404, detail="Contacte no trobat")
    
    db_contacte.notes_humanes = notes_humanes
    db.commit()
    db.refresh(db_contacte)
    return db_contacte
