import os
import sys
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import re
from datetime import datetime, timedelta
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal
import models_v2 as m2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IMAP_HOST = os.getenv("IMAP_HOST", "mail.cdmon.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")
IMAP_SSL = str(os.getenv("IMAP_SSL", "true")).lower() == "true"

def extract_domain(email_addr):
    if not email_addr or "@" not in email_addr:
        return None
    return email_addr.split("@")[-1].lower()

def auto_assign_municipi(db: Session, email_addr: str) -> str:
    from sqlalchemy import or_
    # Buscar ultim email vinculat per trobar el municipi
    prev_email = db.query(m2.EmailV2).filter(
        or_(m2.EmailV2.from_address == email_addr, m2.EmailV2.to_address == email_addr)
    ).order_by(m2.EmailV2.data_enviament.desc()).first()
    
    if prev_email and prev_email.municipi_id:
        return str(prev_email.municipi_id)
        
    # Buscar per contacte
    contacte = db.query(m2.ContacteV2).filter(m2.ContacteV2.email == email_addr).first()
    if contacte and contacte.municipi_id:
        return str(contacte.municipi_id)
            
    # Buscar per domini web del municipi
    domain = extract_domain(email_addr)
    if domain and domain not in ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]:
        municipis = db.query(m2.MunicipiLifecycle).all()
        for m in municipis:
            if m.web and domain in m.web.lower():
                return str(m.id)
    return None

def decode_mime_header(raw_header):
    if not raw_header:
        return ""
    decoded_fragments = decode_header(raw_header)
    header_str = ""
    for frag, enc in decoded_fragments:
        if isinstance(frag, bytes):
            header_str += frag.decode(enc or 'utf-8', errors='replace')
        else:
            header_str += str(frag)
    return header_str

def extract_email_address(full_address):
    match = re.search(r'<([^>]+)>', full_address)
    if match:
        return match.group(1).strip()
    return full_address.strip()

def sync_mailbox(folder="INBOX", direccio="IN", search_criteria="UNSEEN"):
    if not IMAP_HOST or not IMAP_USER:
        logger.warning(f"IMAP settings missing, skipping sync {direccio}")
        return
        
    db = SessionLocal()
    mail = None
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) if IMAP_SSL else imaplib.IMAP4(IMAP_HOST, IMAP_PORT)
        mail.login(IMAP_USER, IMAP_PASSWORD)
        
        status, messages = mail.select(folder)
        if status != "OK":
            if folder != "INBOX":
                for alt_name in ["Sent", "Enviados", "Enviats", "&AOk-nviats", "Sent Items", "INBOX.Sent"]:
                    status, messages = mail.select(f'"{alt_name}"')
                    if status == "OK":
                        break
            if status != "OK":
                logger.error(f"Could not select folder {folder} or its alternatives.")
                return

        status, response = mail.search(None, search_criteria)
        if status != "OK" or not response[0]:
            return
            
        message_ids = response[0].split()
        
        for num in message_ids:
            try:
                status, data = mail.fetch(num, '(RFC822)')
                if status != "OK": continue
                    
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                message_id_extern = msg.get("Message-ID", "").strip()
                
                if message_id_extern and db.query(m2.EmailV2).filter(m2.EmailV2.message_id_extern == message_id_extern).first():
                    continue
                    
                assumpte = decode_mime_header(msg.get("Subject", ""))
                from_address = decode_mime_header(msg.get("From", ""))
                to_address = decode_mime_header(msg.get("To", ""))
                
                try:
                    data_email = parsedate_to_datetime(msg.get("Date"))
                except:
                    from dateutil.tz import tzutc
                    data_email = datetime.now(tzutc())
                    
                clean_from = extract_email_address(from_address)
                clean_to = extract_email_address(to_address)
                
                cos = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() in ["text/plain", "text/html"]:
                            try:
                                body = part.get_payload(decode=True)
                                if body:
                                    cos += body.decode(part.get_content_charset() or 'utf-8', errors='replace')
                            except: pass
                else:
                    try:
                        body = msg.get_payload(decode=True)
                        if body:
                            cos = body.decode(msg.get_content_charset() or 'utf-8', errors='replace')
                    except: pass
                
                target_addr = clean_from if direccio == "IN" else clean_to
                municipi_id = auto_assign_municipi(db, target_addr)
                
                dir_v2 = "entrada" if direccio == "IN" else "sortida"
                
                # 1. Crear registre a emails_v2 (V2 UNIFICAT)
                email_v2 = m2.EmailV2(
                    municipi_id=municipi_id,
                    from_address=clean_from,
                    to_address=clean_to,
                    assumpte=assumpte[:200],
                    cos=cos,
                    direccio=dir_v2,
                    data_enviament=data_email,
                    message_id_extern=message_id_extern,
                    obert=(direccio == "OUT"),
                    respost=(direccio == "IN"),
                    sentiment_resposta=m2.SentimentEnum.neutre if direccio == "IN" else None
                )
                db.add(email_v2)
                
                if municipi_id:
                    # 2. Crear activitat de timeline
                    tipus_act = m2.TipusActivitat.email_rebut if direccio == "IN" else m2.TipusActivitat.email_enviat
                    activitat_v2 = m2.ActivitatsMunicipi(
                        municipi_id=municipi_id,
                        tipus_activitat=tipus_act,
                        data_activitat=data_email,
                        contingut={
                            "subject": assumpte,
                            "from": clean_from,
                            "to": clean_to,
                            "body_preview": cos[:1000]
                        },
                        notes_comercial=f"Email ({direccio}) sincronitzat via IMAP V2"
                    )
                    db.add(activitat_v2)
                
                db.commit()
            except Exception as e:
                logger.error(f"Error processing message {num}: {e}")
                db.rollback()
                
    except Exception as e:
        logger.error(f"Global sync error in {folder}: {e}")
    finally:
        if mail:
            try:
                mail.logout()
            except: pass
        db.close()

def sync_all_emails():
    logger.info("Starting IMAP email sync...")
    sync_mailbox("INBOX", "IN", "UNSEEN")
    
    date_since = (datetime.now() - timedelta(days=2)).strftime("%d-%b-%Y")
    sync_mailbox("Sent", "OUT", f'SINCE "{date_since}"')
    logger.info("IMAP email sync finished.")

if __name__ == "__main__":
    sync_all_emails()
