import json
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from .openrouter_client import call_openrouter
from .agent_manager import kimi_agent
from models_v2 import MunicipiLifecycle, ContacteV2, EmailDraftV2, EstatDraftEnum, CarrecEnum, TrucadaV2, ReunioV2, EmailV2
import logging

logger = logging.getLogger(__name__)

from .agent_kimi_k2 import AgentKimiK2

async def generar_draft(db: Session, municipi: MunicipiLifecycle, tipus: str, contacte: Optional[ContacteV2] = None) -> EmailDraftV2:
    agent = AgentKimiK2(db)
    variants = await agent.redactar_email(municipi.id, contacte.id if contacte else None, tipus)

    if not variants:
        raise ValueError("Error IA generant variants d'email")

    # Escollir la millor basat en score (si l'IA el retorna) o la primera
    millor = variants[0]
    idx_millor = 0
    
    return EmailDraftV2(
        municipi_id=municipi.id,
        contacte_id=contacte.id if contacte else None,
        estat=EstatDraftEnum.esborrany,
        subject=millor.get('subject', 'Proposta PXX'),
        cos=millor.get('cos', ''),
        generat_per_ia=True,
        prompt_utilitzat=f"AgentKimiK2 skill: redactar_email.{tipus}",
        variants_generades=variants,
        variant_seleccionada=idx_millor
    )
