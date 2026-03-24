import json
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from .openrouter_client import call_openrouter
from models_v2 import MunicipiLifecycle, ContacteV2, EmailDraftV2, EstatDraftEnum, CarrecEnum, TrucadaV2, ReunioV2, EmailV2
import logging

logger = logging.getLogger(__name__)

def get_prompt_actor(carrec: Optional[str]) -> str:
    prompts = {
        'alcalde': """
Actuant per a: Alcalde (Visionari). Vol llegat, visibilitat, guanyar eleccions.
Missatge-clau: sobirania digital, control del relat, "el teu municipi al mapa".
Regles: Mai funcionalitats tècniques. Sempre impacte polític i territorial.
To: proximitat, "tu", company de trinxera.
""",
        'tecnic': """
Actuant per a: Tècnic de Turisme/Cultura (Gatekeeper). Abrumado, por a obsolescència.
Missatge-clau: IA Punt d'Or estalvia temps, pàgina en blanc, autonomia.
To: empatia, "sé que tens masses projectes", alleujament.
""",
        'cfo': """
Actuant per a: CFO/Interventor (Blocker). Busca dir NO de forma segura.
Missatge-clau: contracte menor LCSP, RGPD, servidors UE, offboarding ZIP.
To: formal, legal, sense ornaments, risc zero.
"""
    }
    # Map to core categories
    if not carrec:
        return prompts['alcalde']
    c = carrec.lower()
    if 'alcalde' in c:
        return prompts['alcalde']
    elif 'tecnic' in c or 'regidor' in c:
        return prompts['tecnic']
    elif 'cfo' in c or 'interventor' in c:
        return prompts['cfo']
    return prompts['alcalde']

def get_prompt_situacio(tipus: str) -> str:
    prompts = {
        'email_1_prospeccio': """
Situació: Primer contacte. Ganxo patrimoni/digitalització específic.
Regles: Màxim 120 paraules. Zero enllaços. Zero emojis.
Estructura: Ganxo personalitzat -> Dolor subtil -> CTA binari.
""",
        'email_2_dolor': """
Situació: No resposta a email 1. Angle "micròfon apagat".
Regles: Màxim 120 paraules. Zero enllaços.
Estructura: Constatar silenci -> Articular dolor -> FOMO suau -> CTA.
""",
        'email_2_interes': """
Situació: Obert múltiples cops, no resposta. Interès latent.
Regles: Màxim 120 paraules.
Estructura: Notar interès -> Oferir ajuda -> Proposar trucada curta.
""",
        'seguiment_post_demo': """
Situació: Demo realitzada, cal mantenir l'interès actiu.
Regles: Referenciar un moment concret de la demo (generat de forma creïble).
Estructura: Recordar moment clau -> Proposar següent pas -> CTA temporal.
""",
        'compliance_cfo': """
Situació: Blocker legal, necessita seguretat.
Regles: Documentació de conformitat disponible, demanar on enviar-la.
Estructura: Reconèixer preocupació -> Llistar garanties -> Oferir trucada tècnica/legal.
"""
    }
    return prompts.get(tipus, prompts['email_1_prospeccio'])

async def generar_draft(db: Session, municipi: MunicipiLifecycle, tipus: str, contacte: Optional[ContacteV2] = None) -> EmailDraftV2:
    """
    Genera un esborrany d'email de 3 variants utilitzant OpenRouter.
    """
    carrec_str = contacte.carrec.value if contacte and contacte.carrec else 'alcalde'
    prompt_actor = get_prompt_actor(carrec_str)
    prompt_situacio = get_prompt_situacio(tipus)
    
    system_prompt = """Ets un assessor en comunicació B2G expert en vendes a municipis de Catalunya. 
Respons SEMPRE en format JSON vàlid en català amb: 'subject' (String), 'cos' (String), 'angle' (String breu), 'score' (Float entre 0 i 1).
No demanis disculpes, no afegeixis format markdown fora del JSON object.
El cos ha de ser text pur o salts de línia \n."""

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
