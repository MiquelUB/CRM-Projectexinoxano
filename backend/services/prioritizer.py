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

_AI_RECOMMENDATIONS_CACHE = {}  # municipi_id -> {"notes": "...", "data": {...}}

async def eval_municipi_ai(m: MunicipiLifecycle, db: Session):
    """
    Avalua un municipi amb la IA (OpenRouter) per a recomanar acció.
    """
    notes = m.angle_personalitzacio or "Cap nota registrada encara."
    cached = _AI_RECOMMENDATIONS_CACHE.get(str(m.id))

    if cached and cached["notes"] == notes:
         res = cached["data"]
    else:
        # Carregar historial d'interaccions per donar context real de si hi ha hagut contacte
        from models_v2 import EmailV2, TrucadaV2, ReunioV2
        import models # antic

        recent_emails = db.query(EmailV2).filter(EmailV2.municipi_id == m.id).order_by(EmailV2.data_enviament.desc()).limit(3).all()
        recent_calls = db.query(TrucadaV2).filter(TrucadaV2.municipi_id == m.id).order_by(TrucadaV2.data.desc()).limit(3).all()
        
        # Fallback de recerca d'emails antics vinculats als emails dels contactes del municipi
        contactes_emails = [c.email for c in m.contactes if c.email]
        old_emails = []
        if contactes_emails:
             old_emails = db.query(models.Email).filter(models.Email.to_address.in_(contactes_emails)).order_by(models.Email.data_email.desc()).limit(3).all()

        historic_summary = ""
        # 1. Emails nous
        for e in reversed(recent_emails): 
             historic_summary += f"- [Email {e.data_enviament.strftime('%d/%m')}] `{e.assumpte}`: {e.cos[:120].strip()}...\n"
             
        # 2. Emails antics (fallback)
        for e in reversed(old_emails):
             historic_summary += f"- [Email Històric {e.data_email.strftime('%d/%m')}] `{e.assumpte}`: {e.cos[:120].strip() if e.cos else ''}...\n"
             
        for c in reversed(recent_calls):
             historic_summary += f"- [Trucada {c.data.strftime('%d/%m')}] Notes: {c.notes_breus or 'Sense notes'}\n"

        if not historic_summary.strip():
             historic_summary = "Sense interaccions recents registrades."

        system_prompt = """Ets un expert assessor comercial en vendes B2G (administració pública) a Catalunya.
Analitzes l'estat d'un Deal i les darreres anotacions del comercial per determinar l'ACCIÓ SEGÜENT i un 'Score' de prioritat (0 a 100).

TÉ EN COMPTE L'HISTORIAL D'INTERACCIONS:
Si hi ha correus o trucades recents, el deal NO està en fase inicial d'investigació freda, sinó que ja hi ha hagut contacte. 
Valora si s'ha refredat el lead per manca de resposta recent i quina acció emprendre (email de seguiment, trucada de rescat, valorar tancar, etc.)

Respon ÚNICAMENT en format JSON vàlid en català:
{
  "score": <int>,
  "accio_recomanada": "<text curt 3-5 paraules>",
  "tipus_accio": "email" | "trucada" | "altre",
  "rao": "<paràgraf explicant el motiu de la recomanació>"
}"""
        
        user_prompt = f"""MUNICIPI: {m.nom}
Etapa actual: {m.etapa_actual.value}
Temperatura: {m.temperatura.value}
Anotacions del Deal (Llegit per la IA): {notes}

HISTORIAL D'INTERACCIONS RECENT:
{historic_summary}
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        try:
             # utilitzant model per defecte d'OpenRouter
             ai_res = await call_openrouter(messages, json_mode=True)
             res = json.loads(ai_res["content"])
             _AI_RECOMMENDATIONS_CACHE[str(m.id)] = { "notes": notes, "data": res }
        except Exception as e:
             # Fallback estàtic si falla la IA
             res = {
                 "score": 10,
                 "accio_recomanada": "Contactar",
                 "tipus_accio": "altre",
                 "rao": f"IA no disponible. {str(e)}"
             }

    return ActionRecommendation(
        municipi_id=str(m.id),
        nom=m.nom,
        score=res.get("score", 0),
        etapa=m.etapa_actual.value,
        accio_recomanada=res.get("accio_recomanada", "Contactar"),
        rao=res.get("rao", ""),
        tipus_accio=res.get("tipus_accio", "altre"),
        contacte_sugerit_id=str(m.actor_principal_id) if m.actor_principal_id else None
    )

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
    
    # Executar avaluació de IA en paral·lel per a tots els actius
    from database import SessionLocal
    async def _eval_wrapper(m):
        local_db = SessionLocal()
        try:
            return await eval_municipi_ai(m, local_db)
        finally:
            local_db.close()

    tasks = [_eval_wrapper(m) for m in active_municipis]
    recommendations = await asyncio.gather(*tasks)
    
    # Ordenar per score descendent i retornar els TOP
    sorted_recs = sorted(recommendations, key=lambda x: x.score, reverse=True)
    return sorted_recs[:limit]
