from sqlalchemy.orm import Session
from models_v2 import MunicipiLifecycle, EtapaFunnelEnum, TemperaturaEnum, ContacteV2
from datetime import datetime

class ActionRecommendation:
    def __init__(self, municipi_id: str, nom: str, score: int, etapa: str, accio_recomanada: str, rao: str, tipus_accio: str = "altre", contacte_sugerit_id: str = None):
        self.municipi_id = municipi_id
        self.nom = nom
        self.score = score
        self.etapa = etapa
        self.accio_recomanada = accio_recomanada
        self.rao = rao
        self.tipus_accio = tipus_accio
        self.contacte_sugerit_id = contacte_sugerit_id

import json
import asyncio
from .openrouter_client import call_openrouter
from .agent_kimi_k2 import AgentKimiK2

async def get_daily_actions(db: Session, limit: int = 10):
    """
    Motor de Priorització del Dashboard Diari mitjançant IA en Paral·lel.
    """
    active_municipis = db.query(MunicipiLifecycle).filter(
        MunicipiLifecycle.etapa_actual.notin_([
            EtapaFunnelEnum.client,
            EtapaFunnelEnum.perdut,
            EtapaFunnelEnum.pausa
        ])
    ).all()
    
    agent = AgentKimiK2(db)
    
    async def _eval_wrapper(m):
        res = await agent.recomanar_accio(m.id)
        return ActionRecommendation(
            municipi_id=str(m.id),
            nom=m.nom,
            score=res.get("score", 0),
            etapa=m.etapa_actual.value,
            accio_recomanada=res.get("accio", res.get("accio_recomanada", "Contactar")),
            rao=res.get("rao", ""),
            tipus_accio=res.get("tipus", res.get("tipus_accio", "altre")),
            contacte_sugerit_id=str(m.actor_principal_id) if m.actor_principal_id else None
        )

    tasks = [_eval_wrapper(m) for m in active_municipis]
    recommendations = await asyncio.gather(*tasks)
    
    # Ordenar per score descendent i retornar els TOP
    sorted_recs = sorted(recommendations, key=lambda x: x.score, reverse=True)
    return sorted_recs[:limit]
