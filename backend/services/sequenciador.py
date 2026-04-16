
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from models import Municipi, Contacte, EmailSequencia, TipusSequenciaEnum, EstatSequenciaEnum
from .draft_generator import generar_draft
import logging

logger = logging.getLogger(__name__)

async def generar_sequencia_prospeccio(db: Session, municipi_id: UUID, contacte_id: Optional[UUID] = None) -> List[EmailSequencia]:
    municipi = db.query(Municipi).filter(Municipi.id == municipi_id).first()
    if not municipi:
        raise ValueError("Municipi no trobat")

    contacte = None
    if contacte_id:
        contacte = db.query(Contacte).filter(Contacte.id == contacte_id).first()
    if not contacte:
        contacte = db.query(Contacte).filter(
            Contacte.municipi_id == municipi_id, 
            Contacte.actiu == True
        ).order_by(Contacte.principal.desc()).first()

    dia0 = datetime.now(timezone.utc)
    seq = []

    try:
        draft1 = await generar_draft(db, municipi, 'email_1_prospeccio', contacte)
        db.add(draft1)
        db.flush()
        
        seq.append(EmailSequencia(
            municipi_id=municipi_id,
            numero_email=1,
            tipus_sequencia=TipusSequenciaEnum.prospeccio,
            estat=EstatSequenciaEnum.preparat,
            data_programada=dia0,
            draft_id=draft1.id
        ))
    except Exception as e:
        logger.error(f"Error generant email 1: {e}")

    seq.append(EmailSequencia(
        municipi_id=municipi_id,
        numero_email=2,
        tipus_sequencia=TipusSequenciaEnum.prospeccio,
        estat=EstatSequenciaEnum.pendent,
        data_programada=dia0 + timedelta(days=4)
    ))

    seq.append(EmailSequencia(
        municipi_id=municipi_id,
        numero_email=3,
        tipus_sequencia=TipusSequenciaEnum.prospeccio,
        estat=EstatSequenciaEnum.pendent,
        data_programada=dia0 + timedelta(days=8)
    ))

    db.add_all(seq)
    db.commit()
    return seq

async def preparar_email_sequencia(db: Session, municipi_id: UUID, numero_email: int) -> Optional[EmailSequencia]:
    seq = db.query(EmailSequencia).filter(
        EmailSequencia.municipi_id == municipi_id,
        EmailSequencia.numero_email == numero_email
    ).first()

    if not seq or seq.estat != EstatSequenciaEnum.pendent:
        return seq

    municipi = seq.municipi
    contacte = db.query(Contacte).filter(
        Contacte.municipi_id == municipi_id,
        Contacte.actiu == True
    ).order_by(Contacte.principal.desc()).first()

    tipus_map = {
        2: 'email_2_dolor',
        3: 'email_2_interes',
        4: 'compliance_cfo'
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
        logger.error(f"Error preparant email {numero_email}: {e}")
        return None
