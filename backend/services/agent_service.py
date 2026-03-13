import json
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime

from .openrouter_client import call_openrouter
import models

def build_contact_context(db: Session, contacte_id: UUID):
    contacte = db.query(models.Contacte).filter(models.Contacte.id == contacte_id).first()
    if not contacte:
        return None
    
    # Get last 10 emails for context
    emails = db.query(models.Email).filter(models.Email.contacte_id == contacte_id).order_by(models.Email.data_email.desc()).limit(10).all()
    emails = sorted(emails, key=lambda x: x.data_email)
    
    context = f"""CONTEXT DEL CONTACTE:
- Nom: {contacte.nom}
- Càrrec: {contacte.carrec or 'Desconegut'}
- Municipi: {contacte.municipi.nom if contacte.municipi else 'Desconegut'}
- Notes: {contacte.notes_humanes or 'Cap nota'}

FIL D'EMAILS RECENT AMB AQUEST CONTACTE:
"""
    for e in emails:
        dir_text = "REBUT" if e.direccio == "IN" else "ENVIAT"
        cos_breu = (e.cos[:500] + "...") if e.cos and len(e.cos) > 500 else (e.cos or "")
        context += f"--- {dir_text} ({e.data_email.strftime('%d/%m/%Y %H:%M')}) ---\nAssumpte: {e.assumpte}\nCos: {cos_breu}\n\n"
        
    return context

def build_deal_context(db: Session, deal_id: Optional[UUID]):
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        return None
    
    # Get last 10 emails for context
    emails = db.query(models.Email).filter(models.Email.deal_id == deal_id).order_by(models.Email.data_email.desc()).limit(10).all()
    emails = sorted(emails, key=lambda x: x.data_email) # Reorder chronologically
    
    # Get notes
    notes = deal.notes_humanes or "Cap nota registrada."
    
    # Get activities (stage changes)
    activitats = db.query(models.DealActivitat).filter(models.DealActivitat.deal_id == deal_id).order_by(models.DealActivitat.created_at.asc()).all()
    
    context = f"""CONTEXT DEL DEAL:
- Títol: {deal.titol}
- Etapa actual: {deal.etapa}
- Municipi: {deal.municipi.nom} ({deal.municipi.tipus})
- Contacte: {deal.contacte.nom if deal.contacte else 'Desconegut'} - {deal.contacte.carrec if deal.contacte else ''}
- Valor Set Up: {deal.valor_setup} €
- Valor Manteniment: {deal.valor_llicencia} €
- Proper pas actual: {deal.proper_pas or 'Cap'}
- Notes del comercial: {notes}

FIL D'EMAILS RECENT:
"""
    for e in emails:
        dir_text = "REBUT" if e.direccio == "IN" else "ENVIAT"
        cos_breu = (e.cos[:500] + "...") if e.cos and len(e.cos) > 500 else (e.cos or "")
        context += f"--- {dir_text} ({e.data_email.strftime('%d/%m/%Y %H:%M')}) ---\nAssumpte: {e.assumpte}\nCos: {cos_breu}\n\n"

    context += "\nHISTORIAL D'ACTIVITAT:\n"
    for act in activitats:
        context += f"- {act.created_at.strftime('%d/%m/%Y')}: {act.descripcio}\n"
        
    return context

async def redactar_email(db: Session, deal_id: Optional[UUID], instruccions: str, model: str, to_address: str, contacte_id: Optional[UUID] = None):
    context = ""
    if deal_id:
        context = build_deal_context(db, deal_id)
    elif contacte_id:
        context = build_contact_context(db, contacte_id)
    
    if not context:
        context = "No hi ha context previ de deal ni de contacte. L'usuari vol escriure un correu genèric."
    
    system_prompt = """Ets un expert en comunicació B2G amb administracions públiques catalanes. Redactes emails professionals, formals però propers, en català correcte i sense tecnicismes. L'objectiu sempre és avançar el deal cap al tancament.
Mai menciones que ets una IA. Escrius en nom del comercial de Projecte Xino Xano (PXX).
Respon ÚNICAMENT amb el text prose del correu, sense cap format JSON ni etiquetes addicionals. No incloguis l'assumpte dins del cos."""

    user_prompt = f"{context}\n\nINSTRUCCIONS DE L'USUARI: {instruccions or 'Redacta un email de seguiment professional.'}\n\nSi et plau, redacta l'email adreçat a {to_address or 'al contacte'}."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    ai_response = await call_openrouter(messages, model=model, json_mode=False)
    
    # We now expect pure text. The subject can be a generic one or we can try to "guess" it from the first line if the AI 
    # included it despite instructions, but for simplicity we keep it clean.
    return {
        "assumpte": instruccions[:50] if instruccions else "Seguiment Projecte Xino Xano",
        "cos_text": ai_response["content"],
        "model_usat": ai_response["model_usat"],
        "tokens_usats": ai_response["tokens_usats"]
    }

async def analitzar_deal(db: Session, deal_id: UUID, model: str):
    context = build_deal_context(db, deal_id)
    
    system_prompt = """Ets un assessor comercial expert en vendes B2G a administracions públiques. Analitzes el context d'un deal i identifies obstacles reals.
Respons SEMPRE en format JSON vàlid en català amb: 'obstacle_principal', 'proper_pas_recomanat', 'missatge_clau', 'urgencia' (baixa/mitjana/alta)."""

    user_prompt = f"{context}\n\nAnalitza aquest deal i extracta els obstacles i recomanacions."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    ai_response = await call_openrouter(messages, model=model, json_mode=True)
    try:
        res = json.loads(ai_response["content"])
        res["model_usat"] = ai_response["model_usat"]
        return res
    except:
        raise ValueError("L'IA ha retornat un format d'anàlisi no reconegut.")

async def resumir_deal(db: Session, deal_id: UUID, model: str):
    context = build_deal_context(db, deal_id)
    
    system_prompt = "Ets un assistent comercial. Resumeix l'estat d'aquest deal en un paràgraf de màxim 5 línies en català. Sigues molt concret sobre l'última interacció i el proper pas."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": context}
    ]
    
    ai_response = await call_openrouter(messages, model=model)
    return {
        "resum": ai_response["content"],
        "model_usat": ai_response["model_usat"]
    }
