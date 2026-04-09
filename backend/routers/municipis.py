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

router = APIRouter(prefix="/municipis", tags=["municipis"])

@router.get("", response_model=schemas.MunicipiListResponse)
def get_municipis(
    cerca: Optional[str] = None,
    tipus: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.Usuari = Depends(get_current_user)
):
    query = db.query(models.Municipi)
    if cerca:
        query = query.filter(models.Municipi.nom.ilike(f"%{cerca}%"))
    if tipus:
        query = query.filter(models.Municipi.tipus == tipus)
        
    total = query.count()
    items = query.order_by(models.Municipi.nom).offset((page - 1) * limit).limit(limit).all()
    
    return {"items": items, "total": total, "page": page}

@router.get("/{id}", response_model=schemas_v2.MunicipiLifecycleDetailOut)
def get_municipi(id: UUID, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    # Migrat a V2: MunicipiLifecycle
    municipi = db.query(models_v2.MunicipiLifecycle).filter(models_v2.MunicipiLifecycle.id == str(id)).first()
    if not municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat (V2)")
    return municipi

@router.post("", response_model=schemas.MunicipiOut, status_code=status.HTTP_201_CREATED)
def create_municipi(municipi: schemas.MunicipiCreate, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    # Validació de duplicats per Nom + CP
    query = db.query(models.Municipi).filter(models.Municipi.nom == municipi.nom)
    if municipi.codi_postal:
        query = query.filter(models.Municipi.codi_postal == municipi.codi_postal)
        
    if query.first():
        raise HTTPException(status_code=400, detail="Aquest municipi ja està registrat amb aquest nom/CP.")
        
    db_municipi = models.Municipi(**municipi.model_dump())
    db.add(db_municipi)
    db.commit()
    db.refresh(db_municipi)
    return db_municipi

@router.put("/{id}", response_model=schemas.MunicipiOut)
def update_municipi(id: UUID, municipi: schemas.MunicipiUpdate, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_municipi = db.query(models.Municipi).filter(models.Municipi.id == id).first()
    if not db_municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    update_data = municipi.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_municipi, key, value)
        
    db.commit()
    db.refresh(db_municipi)
    return db_municipi

@router.delete("/{id}")
def delete_municipi(id: UUID, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    db_municipi = db.query(models.Municipi).filter(models.Municipi.id == id).first()
    if not db_municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    db.delete(db_municipi)
    db.commit()
    return {"message": "eliminat"}

@router.get("/{id}/deals", response_model=List[schemas.DealOut])
def get_municipi_deals(id: UUID, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    deals = db.query(models.Deal).filter(models.Deal.municipi_id == id).all()
    return deals

@router.get("/{id}/contactes", response_model=List[schemas.ContacteOut])
def get_municipi_contactes(id: UUID, db: Session = Depends(get_db), current_user: models.Usuari = Depends(get_current_user)):
    contactes = db.query(models.Contacte).filter(models.Contacte.municipi_id == id).all()
    return contactes
