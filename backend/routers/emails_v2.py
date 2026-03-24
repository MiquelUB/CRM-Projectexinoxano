from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from models_v2 import MunicipiLifecycle, ContacteV2, EmailDraftV2, EmailSequenciaV2, EstatDraftEnum
from schemas_v2 import EmailDraftCreateRequest, EmailDraftEditRequest, EmailDraftSelectVariantRequest, EmailDraftSendRequest, EmailSequenciaGenerateRequest
from services.draft_generator import generar_draft
from services.sequenciador import generar_sequencia_prospeccio, preparar_email_sequencia
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/emails_v2", tags=["Emails v2"])

@router.post("/drafts/nou/{municipi_id}")
async def crear_draft_endpoint(
    municipi_id: UUID,
    req: EmailDraftCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Genera un nou esborrany d'email mitjançant IA.
    """
    municipi = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == municipi_id).first()
    if not municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat")
    
    contacte = None
    if req.contacte_id:
        contacte = db.query(ContacteV2).filter(ContacteV2.id == req.contacte_id).first()

    try:
        draft = await generar_draft(db, municipi, req.tipus, contacte)
        db.add(draft)
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
    """
    Obté les dades d'un esborrany i les seves variants.
    """
    draft = db.query(EmailDraftV2).filter(EmailDraftV2.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft no trobat")
        
    return {
        'draft_id': draft.id,
        'subject': draft.subject,
        'cos': draft.cos,
        'estat': draft.estat,
        'variants': draft.variants_generades,
        'variant_seleccionada': draft.variant_seleccionada,
        'editat': draft.editat_per_usuari,
        'angle_personalitzacio': draft.municipi.angle_personalitzacio if draft.municipi else None
    }

@router.post("/drafts/{draft_id}/seleccionar_variant")
def seleccionar_variant_endpoint(
    draft_id: UUID,
    req: EmailDraftSelectVariantRequest,
    db: Session = Depends(get_db)
):
    """
    Commuta l'esborrany a una de les variants alternatives de l'IA.
    """
    draft = db.query(EmailDraftV2).filter(EmailDraftV2.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft no trobat")
    
    if req.variant_id < 0 or req.variant_id >= len(draft.variants_generades):
        raise HTTPException(status_code=400, detail="Variant ID no existent")

    variant = draft.variants_generades[req.variant_id]
    draft.variant_seleccionada = req.variant_id
    draft.subject = variant.get('subject')
    draft.cos = variant.get('cos')
    
    db.commit()
    return {'status': 'variant_canviada', 'subject': draft.subject}

@router.post("/drafts/{draft_id}/editar")
def editar_draft_endpoint(
    draft_id: UUID,
    req: EmailDraftEditRequest,
    db: Session = Depends(get_db)
):
    """
    Guarda canvis manuals realitzats per l'usuari.
    """
    draft = db.query(EmailDraftV2).filter(EmailDraftV2.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft no trobat")

    draft.subject = req.subject
    draft.cos = req.cos
    draft.editat_per_usuari = True
    draft.canvis_respecte_ia = req.canvis
    
    db.commit()
    return {'status': 'guardat'}

@router.post("/drafts/{draft_id}/enviar")
def enviar_draft_endpoint(
    draft_id: UUID,
    req: EmailDraftSendRequest,
    db: Session = Depends(get_db)
):
    """
    Envia immediatament o programa un draft.
    """
    draft = db.query(EmailDraftV2).filter(EmailDraftV2.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft no trobat")

    # MOCK d'enviament SMTP
    if req.mode == 'immediat':
        draft.estat = EstatDraftEnum.enviat
        draft.data_enviament = datetime.utcnow()
    else:
        draft.estat = EstatDraftEnum.programat
        draft.data_enviament = req.data_programada

    db.commit()
    return {'status': 'enviat' if req.mode == 'immediat' else 'programat'}

@router.post("/enviar_manual/{municipi_id}")
def enviar_manual_endpoint(
    municipi_id: UUID,
    req: EmailDraftEditRequest,  # reusing subject, cos body schema
    db: Session = Depends(get_db)
):
    """
    Crea i desa un email manualment (sense draft prèvia ni IA).
    """
    from models_v2 import EmailV2
    
    municipi = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == municipi_id).first()
    if not municipi:
        raise HTTPException(status_code=404, detail="Municipi no trobat")

    # Guardar a l'històric d'emails enviats
    nou_email = EmailV2(
        municipi_id=municipi_id,
        assumpte=req.subject,
        cos=req.cos,
        data_enviament=datetime.utcnow()
    )
    db.add(nou_email)
    db.commit()
    return {"status": "enviat_manualment"}

@router.post("/sequencia/generar/{municipi_id}")
async def generar_sequencia_endpoint(
    municipi_id: UUID,
    req: EmailSequenciaGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Genera seqüència de correus automatitzats basats en prospecció.
    """
    try:
        seq = await generar_sequencia_prospeccio(db, municipi_id, req.contacte_id)
        return {
            'municipi_id': municipi_id,
            'emails_generats': len(seq),
            'calendari': [{'numero': s.numero_email, 'data': s.data_programada, 'estat': s.estat} for s in seq]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
