from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Optional
from models_v2 import MunicipiLifecycle, ContacteV2, EmailSequenciaV2, TipusSequenciaEnum, EstatSequenciaEnum
from .draft_generator import generar_draft
import logging

logger = logging.getLogger(__name__)

async def generar_sequencia_prospeccio(db: Session, municipi_id: UUID, contacte_id: Optional[UUID] = None) -> List[EmailSequenciaV2]:
    """
    Genera la seqüència completa de prospecció per a un municipi nou.
    """
    municipi = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == municipi_id).first()
    if not municipi:
        raise ValueError("Municipi no trobat")

    contacte = None
    if contacte_id:
        contacte = db.query(ContacteV2).filter(ContacteV2.id == contacte_id).first()
    if not contacte:
        # Trobar contacte principal o el primer actiu si no n'hi ha cap
        contacte = db.query(ContacteV2).filter(
            ContacteV2.municipi_id == municipi_id, 
            ContacteV2.actiu == True
        ).order_by(ContacteV2.principal.desc()).first()

    dia0 = datetime.utcnow()
    seq = []

    # EMAIL 1: Primer contacte directe (Prospecció)
    try:
        draft1 = await generar_draft(db, municipi, 'email_1_prospeccio', contacte)
        db.add(draft1)
        db.flush() # Per obtenir l'ID del draft1 immediatament
        
        seq.append(EmailSequenciaV2(
            municipi_id=municipi_id,
            numero_email=1,
            tipus_sequencia=TipusSequenciaEnum.prospeccio,
            estat=EstatSequenciaEnum.preparat,
            data_programada=dia0,
            draft_id=draft1.id
        ))
    except Exception as e:
        logger.error(f"No s'ha pogut generar el primer email draft de la seqüència: {e}")

    # EMAIL 2: Dolor / Angle micròfon (Programat a +4 dies)
    seq.append(EmailSequenciaV2(
        municipi_id=municipi_id,
        numero_email=2,
        tipus_sequencia=TipusSequenciaEnum.prospeccio,
        estat=EstatSequenciaEnum.pendent,
        data_programada=dia0 + timedelta(days=4)
    ))

    # EMAIL 3: FOMO veïns (Programat a +8 dies)
    seq.append(EmailSequenciaV2(
        municipi_id=municipi_id,
        numero_email=3,
        tipus_sequencia=TipusSequenciaEnum.prospeccio,
        estat=EstatSequenciaEnum.pendent,
        data_programada=dia0 + timedelta(days=8)
    ))

    # EMAIL 4: Recuperació (Programat a +14 dies)
    seq.append(EmailSequenciaV2(
        municipi_id=municipi_id,
        numero_email=4,
        tipus_sequencia=TipusSequenciaEnum.recuperacio,
        estat=EstatSequenciaEnum.pendent,
        data_programada=dia0 + timedelta(days=14)
    ))

    db.add_all(seq)
    db.commit()
    return seq

async def preparar_email_sequencia(db: Session, municipi_id: UUID, numero_email: int) -> Optional[EmailSequenciaV2]:
    """
    Genera el draft d'un email que estava en estat 'pendent'.
    """
    seq = db.query(EmailSequenciaV2).filter(
        EmailSequenciaV2.municipi_id == municipi_id,
        EmailSequenciaV2.numero_email == numero_email
    ).first()

    if not seq or seq.estat != EstatSequenciaEnum.pendent:
        return seq # Ja preparat o inexistent

    municipi = seq.municipi
    contacte = db.query(ContacteV2).filter(
        ContacteV2.municipi_id == municipi_id,
        ContacteV2.actiu == True
    ).order_by(ContacteV2.principal.desc()).first()

    # Determinar el tipus adequat de la llista de situacions de draft
    tipus_map = {
        2: 'email_2_dolor',
        3: 'email_2_interes', # placeholder alternatiu 
        4: 'compliance_cfo'   # placeholder alternatiu 
    }
    tipus_draft = tipus_map.get(numero_email, 'email_1_prospeccio')

    try:
        draft = await generar_draft(db, municipi, tipus_draft, contacte)
        db.add(draft)
        db.flush()

        seq.draft_id = draft.id
        seq.estat = EstatSequenciaEnum.preparat
        db.commit()
        return seq
    except Exception as e:
        logger.error(f"Error preparant email {numero_email} per seqüència: {e}")
        return None
