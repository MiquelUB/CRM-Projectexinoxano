from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database import get_db
import models
import schemas
from auth import get_current_user, get_password_hash

router = APIRouter(prefix="/usuaris", tags=["usuaris"])

@router.get("/", response_model=List[schemas.UsuariOut])
def llistar_usuaris(
    current_user: models.Usuari = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No tens permisos per veure els usuaris")
    return db.query(models.Usuari).all()

@router.post("/", response_model=schemas.UsuariOut)
def crear_usuari(
    usuari: schemas.UsuariCreate,
    current_user: models.Usuari = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No tens permisos per crear usuaris")
    
    db_user = db.query(models.Usuari).filter(models.Usuari.email == usuari.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="L'email ja està registrat")
    
    new_user = models.Usuari(
        email=usuari.email,
        password_hash=get_password_hash(usuari.password),
        nom=usuari.nom,
        rol=usuari.rol,
        actiu=usuari.actiu
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.patch("/{usuari_id}", response_model=schemas.UsuariOut)
def editar_usuari(
    usuari_id: UUID,
    usuari_data: dict, # Simplified update
    current_user: models.Usuari = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No tens permisos per editar usuaris")
    
    db_user = db.query(models.Usuari).filter(models.Usuari.id == usuari_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    
    if "password" in usuari_data and usuari_data["password"]:
        db_user.password_hash = get_password_hash(usuari_data["password"])
    
    if "email" in usuari_data: db_user.email = usuari_data["email"]
    if "nom" in usuari_data: db_user.nom = usuari_data["nom"]
    if "rol" in usuari_data: db_user.rol = usuari_data["rol"]
    if "actiu" in usuari_data: db_user.actiu = usuari_data["actiu"]
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{usuari_id}")
def eliminar_usuari(
    usuari_id: UUID,
    current_user: models.Usuari = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No tens permisos per eliminar usuaris")
    
    db_user = db.query(models.Usuari).filter(models.Usuari.id == usuari_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    
    if db_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="No et pots eliminar a tu mateix")
        
    db.delete(db_user)
    db.commit()
    return {"message": "Usuari eliminat correctament"}
