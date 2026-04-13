from sqlalchemy.orm import Session
from models_v2 import MunicipiLifecycle, EtapaFunnelEnum, TemperaturaEnum, ContacteV2
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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

async def get_daily_actions(db: Session, limit: int = 10):
    """
    Motor de Priorització del Dashboard Diari.
    (Actulizat per ser instanci i no bloquejar per cridades a la IA massives).
    """
    active_municipis = db.query(MunicipiLifecycle).filter(
        MunicipiLifecycle.etapa_actual.notin_([
            EtapaFunnelEnum.client,
            EtapaFunnelEnum.perdut,
            EtapaFunnelEnum.pausa
        ])
    ).all()
    
    recommendations = []
    for m in active_municipis:
        score = 0
        accio = "Contactar per reprendre tema."
        tipus = "trucada"
        
        # 1. Base Score depending on Etapa
        if m.etapa_actual == EtapaFunnelEnum.aprovacio:
            score += 50
            accio = "Preguntar si han pogut avaluar-ho."
            tipus = "trucada"
        elif m.etapa_actual == EtapaFunnelEnum.oferta:
            score += 40
            accio = "Fer seguiment de l'oferta enviada."
            tipus = "email"
        elif m.etapa_actual == EtapaFunnelEnum.demo_ok:
            score += 30
            accio = "Enviar proposta econòmica."
            tipus = "email"
        elif m.etapa_actual == EtapaFunnelEnum.contacte:
            score += 20
            accio = "Trucar per agendar Demo."
            tipus = "trucada"
            
        # 2. Add priority multiplier
        if m.prioritat == "alta":
            score += 30
        elif m.prioritat == "mitjana":
            score += 15
            
        # 3. Add hotness multiplier
        if m.temperatura == TemperaturaEnum.bullent:
            score += 20
            accio = "Tancar acord!"
        elif m.temperatura == TemperaturaEnum.calent:
            score += 10
            
        etapa_label = m.etapa_actual.value if m.etapa_actual else "desconeguda"
        
        recommendations.append(
            ActionRecommendation(
                municipi_id=str(m.id),
                nom=m.nom,
                score=score,
                etapa=etapa_label,
                accio_recomanada=accio,
                rao=f"Etapa {etapa_label} amb prioritat {m.prioritat}.",
                tipus_accio=tipus,
                contacte_sugerit_id=str(m.actor_principal_id) if m.actor_principal_id else None
            )
        )
        
    sorted_recs = sorted(recommendations, key=lambda x: x.score, reverse=True)
    return sorted_recs[:limit]
