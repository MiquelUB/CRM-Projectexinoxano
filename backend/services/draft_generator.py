
import json
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from .openrouter_client import call_openrouter
from .agent_manager import kimi_agent
from models import Municipi, Contacte, EmailDraft, Email
import logging

logger = logging.getLogger(__name__)

from .agent_kimi_k2 import AgentKimiK2

async def generar_draft(db: Session, municipi: Municipi, tipus: str, contacte: Optional[Contacte] = None) -> EmailDraft:
    agent = AgentKimiK2(db)
    variants = await agent.redactar_email(municipi.id, contacte.id if contacte else None, tipus)

    if not variants:
        raise ValueError("Error IA generant variants d'email")

    millor = variants[0]
    idx_millor = 0
    
    return EmailDraft(
        municipi_id=municipi.id,
        contacte_id=contacte.id if contacte else None,
        subject=millor.get('subject', 'Proposta PXX'),
        cos=millor.get('cos', ''),
        generat_per_ia=True,
        prompt_utilitzat=f"AgentKimiK2 skill: redactar_email.{tipus}",
        variants_generades=variants,
        variant_seleccionada=idx_millor
    )
