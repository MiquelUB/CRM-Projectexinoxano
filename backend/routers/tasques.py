from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Tasca, Deal
from schemas import TascaCreate, TascaUpdate, TascaOut, TascaListResponse
from uuid import UUID
from typing import List, Optional
from datetime import date, datetime

router = APIRouter(prefix="/tasques", tags=["Tasques"])

from fastapi.encoders import jsonable_encoder

@router.get("/")
def get_tasques(
    deal_id: Optional[UUID] = None, 
    municipi_id: Optional[UUID] = None,
    estat: Optional[str] = None,
    data_inici: Optional[date] = None,
    data_fi: Optional[date] = None,
    db: Session = Depends(get_db)
):
    try:
        # 1. Get explicit tasks
        query = db.query(Tasca)
        if deal_id:
            query = query.filter(Tasca.deal_id == deal_id)
        if municipi_id:
            query = query.filter(Tasca.municipi_id == municipi_id)
        if estat:
            query = query.filter(Tasca.estat == estat)
        if data_inici:
            query = query.filter(Tasca.data_venciment >= data_inici)
        if data_fi:
            query = query.filter(Tasca.data_venciment <= data_fi)
            
        tasques = query.order_by(Tasca.data_venciment.asc()).all()
        
        # 2. Get deal follow-ups (pseudo-tasks)
        from sqlalchemy.orm import joinedload
        deal_query = db.query(Deal).options(
            joinedload(Deal.municipi),
            joinedload(Deal.contacte)
        ).filter(Deal.data_seguiment.is_not(None))
        
        if deal_id:
            deal_query = deal_query.filter(Deal.id == deal_id)
        if municipi_id:
            deal_query = deal_query.filter(Deal.municipi_id == municipi_id)
        if data_inici:
            deal_query = deal_query.filter(Deal.data_seguiment >= data_inici)
        if data_fi:
            deal_query = deal_query.filter(Deal.data_seguiment <= data_fi)
        
        deals_with_followup = deal_query.all()
        
        pseudo_tasques = []
        for d in deals_with_followup:
            if d.etapa in ['guanyat', 'perdut', 'tancat_guanyat']:
                continue
                
            tipus = "altre"
            pp = (d.proper_pas or "").lower()
            if "trucada" in pp or "trucar" in pp or "call" in pp:
                tipus = "trucada"
            elif "email" in pp or "enviar" in pp or "correu" in pp:
                tipus = "email"
            elif "demo" in pp or "presentaci" in pp:
                tipus = "demo"
            elif "reunio" in pp or "reunió" in pp or "meeting" in pp:
                tipus = "reunio"

            # Context enrichment
            nom_municipi = d.municipi.nom if d.municipi else "Desconegut"
            nom_contacte = d.contacte.nom if d.contacte else ""
            
            pseudo_tasques.append({
                "id": str(d.id), 
                "titol": d.proper_pas or f"Seguiment: {d.titol}",
                "descripcio": f"Deal: {d.titol} ({nom_municipi})" + (f" - {nom_contacte}" if nom_contacte else ""),
                "data_venciment": d.data_seguiment,
                "tipus": tipus,
                "prioritat": d.prioritat or "mitjana",
                "estat": "pendent",
                "deal_id": d.id,
                "municipi_id": d.municipi_id,
                "contacte_id": d.contacte_id,
                "entitat_nom": nom_municipi,
                "contacte_nom": nom_contacte,
                "created_at": d.created_at,
                "updated_at": d.updated_at,
                "is_pseudo": True
            })
        
        all_items = []
        for t in tasques:
            # For real tasks, we would ideally joinedload them too
            # Let's do a quick fetch of names if possible or just use what we have
            all_items.append({
                "id": t.id,
                "titol": t.titol,
                "descripcio": t.descripcio,
                "data_venciment": t.data_venciment,
                "tipus": t.tipus,
                "prioritat": t.prioritat,
                "estat": t.estat,
                "deal_id": t.deal_id,
                "municipi_id": t.municipi_id,
                "contacte_id": t.contacte_id,
                "entitat_nom": t.municipi.nom if t.municipi else "",
                "contacte_nom": t.contacte.nom if t.contacte else "",
                "created_at": t.created_at,
                "updated_at": t.updated_at,
                "is_pseudo": False
            })
        
        all_items.extend(pseudo_tasques)
        
        # Robust sort (handle None just in case)
        all_items.sort(key=lambda x: x["data_venciment"] if x["data_venciment"] else date.max)
        
        return jsonable_encoder({"items": all_items, "total": len(all_items)})
    except Exception as e:
        print(f"ERROR in get_tasques: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=TascaOut)
def create_tasca(tasca_in: TascaCreate, db: Session = Depends(get_db)):
    tasca = Tasca(**tasca_in.model_dump())
    db.add(tasca)
    db.commit()
    db.refresh(tasca)
    return tasca

@router.patch("/{id}", response_model=TascaOut)
def update_tasca(id: UUID, tasca_in: TascaUpdate, db: Session = Depends(get_db)):
    tasca = db.query(Tasca).filter(Tasca.id == id).first()
    if not tasca:
        raise HTTPException(status_code=404, detail="Tasca not found")
        
    update_data = tasca_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tasca, key, value)
        
    db.commit()
    db.refresh(tasca)
    return tasca

@router.delete("/{id}")
def delete_tasca(id: UUID, db: Session = Depends(get_db)):
    tasca = db.query(Tasca).filter(Tasca.id == id).first()
    if not tasca:
        raise HTTPException(status_code=404, detail="Tasca not found")
    
    db.delete(tasca)
    db.commit()
    return {"message": "Tasca eliminada correctament"}
