---
name: email-imap-integration
description: Guides IMAP/SMTP email integration with CDmon for CRM PXX. Use when implementing email synchronization, sending emails from the CRM, linking emails to deals, or building the email marketing campaign module. Covers both incoming (INBOX) and outgoing (Sent folder) sync.
---

# Integració Email IMAP/SMTP — CDmon

Aplica aquest skill quan treballis en qualsevol funcionalitat relacionada amb el correu.

## Configuració CDmon

```python
# Variables d'entorn requerides (.env)
IMAP_HOST=mail.cdmon.com
IMAP_PORT=993
IMAP_USER=crm@projectexinoxano.cat
IMAP_PASSWORD=contrasenya_segura
IMAP_USE_SSL=true

SMTP_HOST=mail.cdmon.com
SMTP_PORT=587
SMTP_USER=crm@projectexinoxano.cat
SMTP_PASSWORD=contrasenya_segura
SMTP_USE_TLS=true
```

## Principi Fonamental: Fils Complets IN + OUT

L'agent IA necessita veure TOTA la conversa. El sistema sincronitza SEMPRE les dues carpetes:

| Carpeta IMAP | Direcció | Descripció |
|---|---|---|
| INBOX | IN | Emails rebuts del client/ajuntament |
| Sent / Enviats | OUT | Emails enviats des de Thunderbird |
| CRM-Sent (carpeta pròpia) | OUT | Emails enviats des del CRM |

**Regla crítica:** Si només es sincronitza INBOX, l'agent IA veu la meitat de la conversa i els seus suggeriments seran incorrectes.

## Sincronització IMAP (Python)

```python
import imaplib
import email
from email.header import decode_header

def sync_emails(db: Session):
    """Sincronitza INBOX i Sent. Crida cada 5 minuts via scheduler."""
    with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) as imap:
        imap.login(IMAP_USER, IMAP_PASSWORD)

        # Sincronitzar emails REBUTS
        imap.select("INBOX")
        _process_folder(imap, db, direccio="IN")

        # Sincronitzar emails ENVIATS (Thunderbird)
        # Prova els dos noms possibles de carpeta Sent
        for sent_folder in ["Sent", "Enviats", "INBOX.Sent"]:
            try:
                imap.select(sent_folder)
                _process_folder(imap, db, direccio="OUT")
                break
            except:
                continue

def _process_folder(imap, db, direccio: str):
    _, message_ids = imap.search(None, "UNSEEN")
    for msg_id in message_ids[0].split():
        _, msg_data = imap.fetch(msg_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        _save_email(msg, db, direccio)
```

## Vinculació Automàtica Email → Deal

L'algoritme de vinculació segueix aquest ordre de prioritat:

```python
def vincular_deal(email_from: str, email_to: str, db: Session):
    """
    Prioritat de vinculació:
    1. Historial: busca si aquest email ja apareix en emails anteriors d'un deal
    2. Domini: busca municipis amb el mateix domini (@ajleida.cat → Lleida)
    3. Contacte: busca contactes amb aquest email exacte
    4. Manual: si no troba res, el deixa sense vincular per assignació manual
    """
    address = email_from if direccio == "IN" else email_to
    domain = address.split("@")[-1]

    # 1. Historial previ
    existing = db.query(Email).filter(Email.from_address == address).first()
    if existing and existing.deal_id:
        return existing.deal_id

    # 2. Domini municipal
    municipi = db.query(Municipi).filter(Municipi.web.contains(domain)).first()
    if municipi:
        deal = db.query(Deal).filter(
            Deal.municipi_id == municipi.id,
            Deal.etapa.notin_(["tancat_guanyat", "perdut"])
        ).first()
        if deal:
            return deal.id

    # 3. Contacte directe
    contacte = db.query(Contacte).filter(Contacte.email == address).first()
    if contacte:
        deal = db.query(Deal).filter(Deal.contacte_id == contacte.id).first()
        if deal:
            return deal.id

    return None  # Assignació manual necessària
```

## Enviament SMTP des del CRM

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(to: str, subject: str, body_html: str, deal_id: str, db: Session):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to

    msg.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    # Guardar a BD com a OUT
    nou_email = Email(
        deal_id=deal_id,
        from_address=SMTP_USER,
        to_address=to,
        assumpte=subject,
        cos=body_html,
        direccio="OUT",
        sincronitzat=True
    )
    db.add(nou_email)
    db.commit()
```

## Scheduler de Sincronització

```python
# Afegir a main.py — sincronització cada 5 minuts
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(sync_emails, "interval", minutes=5, args=[next(get_db())])
scheduler.start()
```

## Taula emails — Camps Clau

| Camp | Tipus | Descripció |
|---|---|---|
| id | UUID | Identificador únic |
| deal_id | UUID FK | Deal associat (pot ser NULL si no vinculat) |
| contacte_id | UUID FK | Contacte associat |
| campanya_id | UUID FK | Campanya associada (si és màrqueting) |
| from_address | VARCHAR | Adreça remitent |
| to_address | VARCHAR | Adreça destinatari |
| assumpte | VARCHAR | Assumpte de l'email |
| cos | TEXT | Cos complet (HTML o text pla) |
| direccio | VARCHAR | Valors: 'IN' o 'OUT' |
| llegit | BOOLEAN | Si ha estat llegit al CRM |
| sincronitzat | BOOLEAN | Si ve d'IMAP o enviat des del CRM |
| data_email | TIMESTAMPTZ | Data real de l'email (del header) |
