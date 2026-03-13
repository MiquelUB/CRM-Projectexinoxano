---
name: openrouter-ai-agent
description: Guides integration of OpenRouter AI API for CRM PXX intelligent features. Use when implementing any AI-powered functionality including deal analysis, email drafting, conversation summarization, or next-step suggestions. Never use OpenAI directly — always use OpenRouter.
---

# OpenRouter AI Agent — CRM PXX

Aplica aquest skill per a QUALSEVOL integració d'IA al CRM.

## Regla Absoluta

**MAI usar OpenAI directament.** Sempre OpenRouter.
La URL base és: `https://openrouter.ai/api/v1`
El format és compatible amb l'API d'OpenAI, però la URL i la key canvien.

## Configuració Base

```python
# .env
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Capçaleres obligatòries d'OpenRouter
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://crm.projectexinoxano.cat",
    "X-Title": "CRM Projecte Xino Xano",
    "Content-Type": "application/json"
}
```

## Client OpenRouter (reutilitzable)

```python
import httpx
from typing import Optional

async def cridar_openrouter(
    prompt: str,
    system_prompt: str,
    model: Optional[str] = None,  # Si None, el caller especifica
    max_tokens: int = 1000
) -> str:
    """
    Client base per a totes les crides a OpenRouter.
    El model es passa per paràmetre — mai hard-coded.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens
            },
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
```

## Selecció de Model per Tasca

El model NO és fix. Es passa com a paràmetre i es decideix en temps d'execució:

| Tasca | Model recomanat | Justificació |
|---|---|---|
| Anàlisi i suggeriment tancament | anthropic/claude-3.5-sonnet | Millor comprensió de context llarg |
| Redacció emails professionals | anthropic/claude-3.5-sonnet | Millor català i to formal B2G |
| Resum executiu de deal | mistralai/mistral-small | Ràpid i econòmic per resums |
| Classificació ràpida leads | meta-llama/llama-3.1-8b-instruct | Barat per tasques simples |
| Anàlisi sentiment resposta | mistralai/mistral-small | GDPR europeu, rendiment adequat |

## Cas d'Ús 1: Suggeriment de Tancament

```python
async def suggeriment_tancament(deal_id: str, db: Session, model: str) -> str:
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    emails = db.query(Email).filter(Email.deal_id == deal_id).order_by(Email.data_email).all()

    # Construir context complet
    fil_emails = "\n---\n".join([
        f"[{e.direccio} - {e.data_email}]\nDe: {e.from_address}\n{e.cos[:500]}"
        for e in emails
    ])

    system_prompt = """Ets un assessor comercial expert en vendes B2G a administracions públiques espanyoles.
Analitzes el context complet d'un deal (emails + notes humanes) i proposes el millor pas per tancar-lo.
Respon sempre en català. Sigues directe, concret i accionable."""

    prompt = f"""DEAL: {deal.titol}
MUNICIPI: {deal.municipi.nom} ({deal.municipi.tipus})
ETAPA ACTUAL: {deal.etapa}
VALOR: Setup {deal.valor_setup}€ + Llicència {deal.valor_llicencia}€/any
PROPER PAS ACORDAT: {deal.proper_pas or 'No definit'}

NOTES HUMANES (converses fora del correu):
{deal.notes_humanes or 'Sense notes'}

FIL COMPLET DE CORREUS (IN i OUT):
{fil_emails or 'Sense emails registrats'}

Analitza tota la informació i proposa:
1. Quin és el principal obstacle per tancar aquest deal?
2. Quina és la millor acció concreta per al proper pas?
3. Quin hauria de ser el missatge clau del proper email?"""

    return await cridar_openrouter(prompt, system_prompt, model=model)
```

## Cas d'Ús 2: Redacció Email de Seguiment

```python
async def redactar_email_seguiment(deal_id: str, instruccions: str, model: str, db: Session) -> str:
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    ultims_emails = db.query(Email).filter(
        Email.deal_id == deal_id
    ).order_by(Email.data_email.desc()).limit(5).all()

    system_prompt = """Ets un expert en comunicació B2G amb administracions públiques catalanes.
Redactes emails professionals, formals però propers, en català correcte.
Mai uses tecnicismes innecessaris. Sempre orientats a l'acció."""

    prompt = f"""Redacta un email de seguiment per a:
DESTINATARI: {deal.contacte.nom}, {deal.contacte.carrec}
MUNICIPI: {deal.municipi.nom}
CONTEXT DEL DEAL: Etapa {deal.etapa}, valor {deal.valor_setup + deal.valor_llicencia}€

ÚLTIMS 5 EMAILS DEL FIL:
{chr(10).join([f'[{e.direccio}] {e.assumpte}: {e.cos[:300]}' for e in ultims_emails])}

INSTRUCCIONS ESPECÍFIQUES: {instruccions}

Redacta l'email complet (assumpte + cos). Formal, en català, orientat a avançar el deal."""

    return await cridar_openrouter(prompt, system_prompt, model=model)
```

## Endpoint API per a l'Agent

```python
# routers/agent.py
@router.post("/deals/{deal_id}/suggeriment")
async def obtenir_suggeriment(
    deal_id: UUID,
    model: str = "anthropic/claude-3.5-sonnet",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    resultat = await suggeriment_tancament(str(deal_id), db, model)
    return { "suggeriment": resultat, "model_usat": model }

@router.post("/deals/{deal_id}/redactar-email")
async def redactar_email(
    deal_id: UUID,
    instruccions: str,
    model: str = "anthropic/claude-3.5-sonnet",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    resultat = await redactar_email_seguiment(str(deal_id), instruccions, model, db)
    return { "email_redactat": resultat, "model_usat": model }
```

## Gestió d'Errors

```python
try:
    resultat = await cridar_openrouter(prompt, system_prompt, model=model)
except httpx.TimeoutException:
    raise HTTPException(503, "L'agent IA ha trigat massa. Torna-ho a intentar.")
except httpx.HTTPStatusError as e:
    if e.response.status_code == 429:
        raise HTTPException(429, "Límit de peticions IA assolit. Espera un moment.")
    raise HTTPException(500, "Error en la connexió amb l'agent IA.")
```
