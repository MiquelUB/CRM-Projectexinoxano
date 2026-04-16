
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, Query, Form, Body
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
import traceback

from database import get_db
from models import Municipi, Contacte, Email, EmailDraft, EmailSequencia, TipusActivitat
from schemas import EmailOut, EmailDraftCreateRequest, EmailDraftEditRequest, EmailDraftSelectVariantRequest, EmailDraftSendRequest, EmailSequenciaGenerateRequest

from services.draft_generator import generar_draft
from services.sequenciador import generar_sequencia_prospeccio, preparar_email_sequencia

router = APIRouter(prefix="/emails", tags=["Emails"])

@router.post("/drafts/nou/{municipi_id}")
async def crear_draft_endpoint(
    municipi_id: UUID,
    req: EmailDraftCreateRequest,
    db: Session = Depends(get_db)
):
    municipi = db.query(Municipi).filter(Municipi.id == municipi_id).first()
    if not municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    contacte = None
    if req.contacte_id:
        contacte = db.query(Contacte).filter(Contacte.id == req.contacte_id).first()

    try:
        draft = await generar_draft(db, municipi, req.tipus, contacte)
        db.add(draft)
        municipi.data_ultima_accio = datetime.now(timezone.utc)
        db.commit()
        db.refresh(draft)
        
        return {
            'draft_id': draft.id,
            'variants': draft.variants_generades,
            'subject_inicial': draft.subject,
            'cos_inicial': draft.cos,
            'angle_personalitzacio': municipi.angle_personalitzacio
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/drafts/{draft_id}")
def obtenir_draft(draft_id: UUID, db: Session = Depends(get_db)):
    draft = db.query(EmailDraft).filter(EmailDraft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft no trobat")
        
    return {
        'draft_id': draft.id,
        'subject': draft.subject,
        'cos': draft.cos,
        'variants': draft.variants_generades if hasattr(draft, 'variants_generades') else [],
        'angle_personalitzacio': draft.municipi.angle_personalitzacio if draft.municipi else None
    }

@router.post("/enviar_manual/{municipi_id}")
async def enviar_manual_endpoint(
    municipi_id: UUID,
    subject: str = Form(None),
    cos: str = Form(None),
    req: Optional[EmailDraftEditRequest] = None,
    db: Session = Depends(get_db)
):
    final_subject = subject or (req.subject if req else "")
    final_cos = cos or (req.cos if req else "")
    
    municipi = db.query(Municipi).filter(Municipi.id == municipi_id).first()
    if not municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat")

    nou_email = Email(
        municipi_id=municipi_id,
        assumpte=final_subject,
        cos=final_cos,
        from_address="comercial@projectexinoxano.cat",
        to_address=municipi.email if hasattr(municipi, 'email') and municipi.email else "",
        direccio="OUT",
        data_enviament=datetime.now(timezone.utc),
        llegit=True
    )
    
    if municipi.actor_principal and hasattr(municipi.actor_principal, 'email'):
        nou_email.to_address = municipi.actor_principal.email

    db.add(nou_email)
    municipi.data_ultima_accio = datetime.now(timezone.utc)
    db.commit()
    return {"status": "enviat_manualment"}

@router.get("", response_model=dict)
def llistar_emails(
    page: int = 1,
    direccio: Optional[str] = None,
    llegit: Optional[bool] = None,
    cerca: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Email)
    
    if direccio:
        query = query.filter(Email.direccio == direccio)
    if llegit is not None:
        query = query.filter(Email.llegit == llegit)
    if cerca:
        query = query.filter(
            or_(
                Email.assumpte.ilike(f"%{cerca}%"),
                Email.cos.ilike(f"%{cerca}%"),
                Email.from_address.ilike(f"%{cerca}%"),
                Email.to_address.ilike(f"%{cerca}%")
            )
        )
        
    total = query.count()
    items = query.order_by(Email.data_enviament.desc()).offset((page - 1) * limit).limit(limit).all()
    
    mapped_items = []
    for item in items:
        # Convertir objecte a dict manualment per assegurar formats
        d = {c.name: getattr(item, c.name) for c in item.__table__.columns}
        
        # BLINDATGE DE DATA: Si és nul·la o invàlida, enviem la data actual en format ISO
        data_valida = d.get("data_enviament") or d.get("created_at") or datetime.now(timezone.utc)
        if isinstance(data_valida, datetime):
            d["data_enviament"] = data_valida.isoformat()
        else:
            d["data_enviament"] = str(data_valida)
            
        d["deal_id"] = item.municipi_id
        mapped_items.append(d)

    return {"items": mapped_items, "total": total, "page": page, "pages": (total // limit) + 1}

@router.patch("/{email_id}/llegit")
def marcar_llegit(
    email_id: UUID, 
    payload: dict = Body(...), 
    db: Session = Depends(get_db)
):
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email no trobat")
    
    email.llegit = payload.get("llegit", True)
    db.commit()
    return {"status": "ok", "llegit": email.llegit}

@router.patch("/{email_id}/deal")
def vincular_email_a_municipi(
    email_id: UUID, 
    payload: dict = Body(...), 
    db: Session = Depends(get_db)
):
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email no trobat")
    
    mid = payload.get("deal_id") or payload.get("municipi_id")
    if not mid:
        raise HTTPException(status_code=400, detail="Falta deal_id o municipi_id")
        
    email.municipi_id = UUID(mid) if isinstance(mid, str) else mid
    db.commit()
    return {"status": "vinculat_ok"}

@router.delete("/{email_id}")
def eliminar_email(email_id: UUID, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email no trobat")
    db.delete(email)
    db.commit()
    return {"status": "esborrat_ok"}

@router.post("/sync")
def sync_emails(background_tasks: BackgroundTasks):
    from services.email_sync import sync_all_emails
    background_tasks.add_task(sync_all_emails)
    return {"status": "ok", "missatge": "Sincronització iniciada"}
