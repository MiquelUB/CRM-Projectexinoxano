from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models_v2 import MunicipiLifecycle, ContacteV2, EtapaFunnelEnum, TemperaturaEnum
from schemas_v2 import MunicipiLifecycleOut, MunicipiLifecycleDetailOut, ContacteCreate, ContacteOut, AccioCreate, MunicipiPaginationOut
from typing import List
from datetime import datetime, timezone
from pydantic import BaseModel

class UpdateNotesRequest(BaseModel):
    angle_personalitzacio: str

router = APIRouter(tags=["municipis_v2"])

@router.get("/kpis")
def get_municipis_kpis(db: Session = Depends(get_db)):
    """
    Calcula KPIs del Pipeline V2.
    """
    try:
        from sqlalchemy import func
        
        # 1. Total de municipis actius al funnel (excloent paquets/perduts)
        total_deals = db.query(MunicipiLifecycle).filter(
            MunicipiLifecycle.etapa_actual.notin_([EtapaFunnelEnum.perdut, EtapaFunnelEnum.pausa])
        ).count()
        
        # 2. Valor Total del Pipeline (Setup + Llicència)
        valor_setup = db.query(func.sum(MunicipiLifecycle.valor_setup)).scalar() or 0
        valor_llicencia = db.query(func.sum(MunicipiLifecycle.valor_llicencia)).scalar() or 0
        valor_total = float(valor_setup + valor_llicencia)
        
        # 3. Municipis amb seguiment per a aquest mes
        from datetime import date
        today = date.today()
        start_of_month = date(today.year, today.month, 1)
        if today.month == 12:
            start_of_next_month = date(today.year + 1, 1, 1)
        else:
            start_of_next_month = date(today.year, today.month + 1, 1)
            
        per_tancar = db.query(MunicipiLifecycle).filter(
            MunicipiLifecycle.data_seguiment >= start_of_month,
            MunicipiLifecycle.data_seguiment < start_of_next_month
        ).count()
        
        return {
            "total_deals": total_deals,
            "valor_total_pipeline": valor_total,
            "deals_per_tancar_aquest_mes": per_tancar,
            "deals_sense_activitat_14_dies": 0
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error calculant KPIs: {str(e)}")

@router.get("/", response_model=MunicipiPaginationOut)
def get_municipis(db: Session = Depends(get_db)):
    """
    Llista tots els Municipis en Lifecycle.
    """
    try:
        query = db.query(MunicipiLifecycle)
        total = query.count()
        municipis = query.all()
        
        # Mapper per assegurar que updated_at existeix per al frontend
        for m in municipis:
            if not hasattr(m, 'updated_at') or m.updated_at is None:
                m.updated_at = m.created_at
                
        return {"items": municipis, "total": total}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error llistant municipis: {str(e)}")

@router.get("/contactes")
def get_all_contactes(db: Session = Depends(get_db)):
    """
    Llista tots els contactes de la V2 (municipis_lifecycle).
    """
    query = db.query(ContacteV2)
    return {"items": query.all(), "total": query.count(), "page": 1}

@router.get("/{id}", response_model=MunicipiLifecycleDetailOut)
def get_municipi_detail(id: str, db: Session = Depends(get_db)):
    """
    Obté el detall d'un municipi amb la llista de contactes relacionals.
    """
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    return m

# -- Accions de Transició --

@router.post("/{id}/accio")
def add_lifecycle_action(id: str, payload: AccioCreate, db: Session = Depends(get_db)):
    """
    Afegeix una acció o transició d'etapa on el municipi puja o baixa el funnel.
    Exemple payload: {"accio": "demo_pendent", "notes": "Demana reunió dimecres."}
    Si l'accio coincideix amb un estat d'EtapaFunnelEnum, actualitza etapa_actual.
    """
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")

    # Actualitzar temperatura si es demana
    notes = payload.notes or ""
    accio_lower = payload.accio.lower()

    # Comprovar si l'acció és una nova etapa
    nova_etapa = None
    for enum_val in EtapaFunnelEnum:
        if enum_val.value == accio_lower:
             nova_etapa = enum_val
             break
             
    if nova_etapa:
         # Actulitzar historial JSONB
         historial = list(m.historial_etapes) if m.historial_etapes else []
         historial.append({
              "etapa": m.etapa_actual.value if m.etapa_actual else "unknown",
              "nova_etapa": nova_etapa.value,
              "data": datetime.now(timezone.utc).isoformat(),
              "notes": notes
         })
         m.historial_etapes = historial
         m.etapa_actual = nova_etapa
         m.dies_etapa_actual = 0 # reset dies desde etapa
         m.data_ultima_accio = datetime.now(timezone.utc)
         
    db.commit()
    return {"status": "success", "message": f"Acció '{payload.accio}' registrada para {m.nom}"}


@router.post("/{id}/contactes", response_model=ContacteOut)
def add_contacte_v2(id: str, contact_data: ContacteCreate, db: Session = Depends(get_db)):
    """
    Afegeix un nou ContacteV2 relacional lligat al Municipi.
    """
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")

    # Si es principal, treure principal de l'altre
    if contact_data.principal:
         for c in m.contactes:
              if c.principal:
                   c.principal = False

    c2 = ContacteV2(
        municipi_id=m.id,
        nom=contact_data.nom,
        carrec=contact_data.carrec,
        email=contact_data.email,
        telefon=contact_data.telefon,
        principal=contact_data.principal,
        actiu=True
    )
    db.add(c2)
    db.commit()
    db.refresh(c2)

    if contact_data.principal:
         m.actor_principal_id = c2.id
         db.commit()

    return c2


@router.put("/{id}/actor_principal/{contacte_id}")
def set_actor_principal(id: str, contacte_id: str, db: Session = Depends(get_db)):
    """
    Defineix un contacte com a Actor Principal d'un MunicipiLifecycle.
    """
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")

    # Trobar contacte
    c = db.query(ContacteV2).filter(ContacteV2.id == contacte_id, ContacteV2.municipi_id == m.id).first()
    if not c:
         raise HTTPException(status_code=404, detail="Contacte no trobat per aquest municipi")

    # Treure principal dels altres
    for cont in m.contactes:
         if cont.principal:
              cont.principal = False

    c.principal = True
    m.actor_principal_id = c.id
    
    db.commit()
    return {"status": "success", "message": f"{c.nom} és ara l'actor principal."}

@router.post("/{id}/notes")
def update_notes_municipi_endpoint(id: str, payload: UpdateNotesRequest, db: Session = Depends(get_db)):
    """
    Actualitza les notes / angle de personalització del municipi que la IA llegeix.
    """
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")

    m.angle_personalitzacio = payload.angle_personalitzacio
    db.commit()
    return {"status": "success", "message": "Notes actualitzades d'acord"}

class EtapaUpdate(BaseModel):
    etapa: str

@router.patch("/{id}/etapa")
def canviar_etapa(id: str, payload: EtapaUpdate, db: Session = Depends(get_db)):
    """
    Permet canviar l'etapa (arrossegament del Kanban).
    """
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    for enum_val in EtapaFunnelEnum:
        if enum_val.value == payload.etapa:
            m.etapa_actual = enum_val
            # Update historial
            historial = list(m.historial_etapes) if m.historial_etapes else []
            historial.append({
                "nova_etapa": payload.etapa,
                "data": datetime.now(timezone.utc).isoformat()
            })
            m.historial_etapes = historial
            db.commit()
            return {"status": "success", "nova_etapa": payload.etapa}
            
    raise HTTPException(status_code=400, detail="Etapa invàlida")

@router.put("/{id}")
def update_municipi(id: str, payload: dict, db: Session = Depends(get_db)):
    """
    Permet l'edició de deals.
    """
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    for key, value in payload.items():
        if hasattr(m, key):
            setattr(m, key, value)
            
    db.commit()
    db.refresh(m)
    return m

@router.delete("/{id}")
def delete_municipi(id: str, db: Session = Depends(get_db)):
    """
    Permet l'eliminació dels municipis.
    """
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    db.delete(m)
    db.commit()
    return {"status": "success"}
