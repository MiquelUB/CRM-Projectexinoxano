
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Tasca, Municipi
from schemas import TascaCreate, TascaOut
from uuid import UUID
from typing import List, Optional
from datetime import date, datetime
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/tasques", tags=["Tasques"])

@router.get("/")
def get_tasques(
    municipi_id: Optional[UUID] = None,
    estat: Optional[str] = None,
    data_inici: Optional[date] = None,
    data_fi: Optional[date] = None,
    db: Session = Depends(get_db)
):
    try:
        # 1. Get explicit tasks
        query = db.query(Tasca)
        if municipi_id:
            query = query.filter(Tasca.municipi_id == municipi_id)
        if estat:
            query = query.filter(Tasca.estat == estat)
        if data_inici:
            query = query.filter(Tasca.data_venciment >= data_inici)
        if data_fi:
            query = query.filter(Tasca.data_venciment <= data_fi)
            
        real_tasques = query.order_by(Tasca.data_venciment.asc()).all()
        
        # 2. Get deal follow-ups (pseudo-tasks)
        deal_query = db.query(Municipi).filter(Municipi.data_seguiment.is_not(None))
        if municipi_id:
            deal_query = deal_query.filter(Municipi.id == municipi_id)
        if data_inici:
            deal_query = deal_query.filter(Municipi.data_seguiment >= data_inici)
        if data_fi:
            deal_query = deal_query.filter(Municipi.data_seguiment <= data_fi)
        
        deals_with_followup = deal_query.all()
        
        all_items = []
        
        # Map priority for frontend (int -> str)
        priority_map = {3: "alta", 2: "mitjana", 1: "baixa"}
        
        for t in real_tasques:
            all_items.append({
                "id": t.id,
                "titol": t.titol,
                "descripcio": t.descripcio,
                "data_venciment": t.data_venciment,
                "prioritat": priority_map.get(t.prioritat, "mitjana") if isinstance(t.prioritat, int) else t.prioritat,
                "estat": t.estat,
                "municipi_id": t.municipi_id,
                "entitat_nom": t.municipi.nom if t.municipi else "",
                "is_pseudo": False
            })
            
        for d in deals_with_followup:
            if d.etapa_actual and d.etapa_actual.value in ['perdut', 'pausa']:
                continue
                
            all_items.append({
                "id": str(d.id), 
                "titol": d.proper_pas or f"Seguiment: {d.nom}",
                "descripcio": f"Deal: {d.nom}",
                "data_venciment": d.data_seguiment,
                "prioritat": d.prioritat if isinstance(d.prioritat, str) else priority_map.get(d.prioritat, "mitjana"),
                "estat": "pendent",
                "municipi_id": d.id,
                "entitat_nom": d.nom,
                "is_pseudo": True
            })
        
        all_items.sort(key=lambda x: x["data_venciment"] if x["data_venciment"] else datetime.max)
        
        return {"items": all_items, "total": len(all_items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=TascaOut)
def create_tasca(tasca_in: TascaCreate, db: Session = Depends(get_db)):
    tasca = Tasca(**tasca_in.model_dump())
    db.add(tasca)
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
    return {"message": "Tasca eliminada"}
