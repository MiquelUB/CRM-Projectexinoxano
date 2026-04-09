import json
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from .openrouter_client import call_openrouter
from .agent_manager import kimi_agent
from models_v2 import MunicipiLifecycle, ContacteV2, EmailDraftV2, EstatDraftEnum, CarrecEnum, TrucadaV2, ReunioV2, EmailV2
import logging

logger = logging.getLogger(__name__)

def map_perfil_key(carrec: Optional[str]) -> str:
    if not carrec: return 'alcalde'
    c = carrec.lower()
    if 'alcalde' in c: return 'alcalde'
    if 'tecnic' in c or 'regidor' in c: return 'tecnic'
    if 'cfo' in c or 'interventor' in c: return 'cfo'
    return 'alcalde'

def map_situacio_key(tipus: str) -> str:
    # Mapeig de tipus extern a clau YAML
    mapping = {
        'email_1_prospeccio': 'email_1_prospeccio',
        'email_2_dolor': 'seguiment_fred',
        'email_2_interes': 'seguiment_fred',
        'seguiment_post_demo': 'post_demo',
        'compliance_cfo': 'compliance_cfo'
    }
    return mapping.get(tipus, 'email_1_prospeccio')

async def generar_draft(db: Session, municipi: MunicipiLifecycle, tipus: str, contacte: Optional[ContacteV2] = None) -> EmailDraftV2:
    """
    Genera un esborrany d'email de 3 variants utilitzant OpenRouter.
    """
    carrec_str = contacte.carrec.value if contacte and contacte.carrec else 'alcalde'
    perfil_key = map_perfil_key(carrec_str)
    situacio_key = map_situacio_key(tipus)
    
    system_prompt = kimi_agent.get_skill_system_prompt("redactar_email", perfil=perfil_key, situacio=situacio_key)

    # Obtenir històric recent (notes del deal/comunicacions)
    recent_trucades = db.query(TrucadaV2).filter(TrucadaV2.municipi_id == municipi.id).order_by(TrucadaV2.data.desc()).limit(2).all()
    notes_trucades = [f"- {t.data.strftime('%Y-%m-%d') if t.data else ''}: {t.notes_breus or ''} {f'({t.resum_ia})' if t.resum_ia else ''}" for t in recent_trucades]
    
    recent_reunions = db.query(ReunioV2).filter(ReunioV2.municipi_id == municipi.id).order_by(ReunioV2.data.desc()).limit(2).all()
    notes_reunions = [f"- {r.data.strftime('%Y-%m-%d') if r.data else ''} [{r.tipus or 'reunio'}]: {r.notes_aar or ''}" for r in recent_reunions]

    recent_emails = db.query(EmailV2).filter(EmailV2.municipi_id == municipi.id).order_by(EmailV2.data_enviament.desc()).limit(2).all()
    notes_emails = [f"- {e.data_enviament.strftime('%Y-%m-%d') if e.data_enviament else ''} | Assumpte: {e.assumpte or ''} | Cos: {e.cos[:100] if e.cos else ''}..." for e in recent_emails]

    context_municipi = {
        'nom': municipi.nom,
        'poblacio': municipi.poblacio,
        'diagnostic': municipi.diagnostic_digital or {},
        'angle_personalitzacio': municipi.angle_personalitzacio or 'Millora visibilitat en el sector turístic.'
    }
    
    user_prompt = f"""
CONTEXT MUNICIPAL:
Nom: {context_municipi['nom']}
Població: {context_municipi['poblacio']}
Angle Especial/Anotacions: {context_municipi['angle_personalitzacio']}

HISTÒRIC RECENT (important per continuitat):
Trucades: {", ".join(notes_trucades) if notes_trucades else 'Cap recent'}
Reunions/Demos: {", ".join(notes_reunions) if notes_reunions else 'Cap recent'}
Emails anteriors: {", ".join(notes_emails) if notes_emails else 'Cap recent'}

CONTACTE:
Nom: {contacte.nom if contacte else 'Alcalde/ssa'}
Càrrec: {carrec_str}
To Comunicació preferit: {contacte.to_preferit.value if contacte and contacte.to_preferit else 'formal'}

DIRECTRIUS DE COMUNICACIÓ:
{prompt_actor}
{prompt_situacio}

Si us plau, redacta l'email.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    variants = []
    # Generem 3 variants amb càrrega de temperatura incremental per trobar varietat
    for i in range(3):
        try:
            temp = 0.5 + (i * 0.2)
            try:
                ai_response = await call_openrouter(messages, model="moonshotai/kimi-k2", json_mode=True, temperature=temp)
            except Exception as e:
                logger.warning(f"Kimi K2 fallit a variant {i+1}, provant Qwen... Error: {e}")
                ai_response = await call_openrouter(messages, model="qwen/qwen-2.5-72b-instruct", json_mode=True, temperature=temp)
                
            res = json.loads(ai_response["content"])
            variants.append({
                'subject': res.get('subject', 'Proposta Projecte Xino Xano'),
                'cos': res.get('cos', ''),
                'angle': res.get('angle', f'Variant {i+1}'),
                'score': res.get('score', 0.8)
            })
        except Exception as e:
            logger.error(f"Error generant variant {i+1}: {e}")

    if not variants:
        raise ValueError("L'IA no ha pogut generar cap variant d'esborrany satisfactòria.")

    # Seleccionar millor variant per defecte
    millor = max(variants, key=lambda x: x['score'])
    idx_millor = variants.index(millor)

    draft = EmailDraftV2(
        municipi_id=municipi.id,
        contacte_id=contacte.id if contacte else None,
        estat=EstatDraftEnum.esborrany,
        subject=millor['subject'],
        cos=millor['cos'],
        generat_per_ia=True,
        prompt_utilitzat=f"{prompt_actor}\n{prompt_situacio}",
        variants_generades=variants,
        variant_seleccionada=idx_millor
    )

    return draft
