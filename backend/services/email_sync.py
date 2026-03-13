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
from models import Email, Deal, Contacte, Municipi

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

def auto_assign_deal(db: Session, email_addr: str) -> str:
    from sqlalchemy import or_
    prev_email = db.query(Email).filter(
        or_(Email.from_address == email_addr, Email.to_address == email_addr),
        Email.deal_id.isnot(None)
    ).order_by(Email.data_email.desc()).first()
    
    if prev_email and prev_email.deal and prev_email.deal.etapa != "tancat_perdut":
        return str(prev_email.deal_id)
        
    contacte = db.query(Contacte).filter(Contacte.email == email_addr).first()
    if contacte:
        deal = db.query(Deal).filter(
            Deal.municipi_id == contacte.municipi_id,
            Deal.etapa != "tancat_perdut"
        ).order_by(Deal.created_at.desc()).first()
        if deal:
            return str(deal.id)
            
    domain = extract_domain(email_addr)
    if domain and domain not in ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]:
        municipis = db.query(Municipi).all()
        for m in municipis:
            if m.web and domain in m.web.lower():
                deal = db.query(Deal).filter(
                    Deal.municipi_id == m.id,
                    Deal.etapa != "tancat_perdut"
                ).order_by(Deal.created_at.desc()).first()
                if deal:
                    return str(deal.id)
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
                for alt_name in ["Sent", "Enviados", "Enviats", "&AOk-nviats", "Sent Items"]:
                    status, messages = mail.select(f'"{alt_name}"')
                    if status == "OK":
                        break
            if status != "OK":
                logger.error(f"Could not select folder {folder}")
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
                
                if message_id_extern and db.query(Email).filter(Email.message_id_extern == message_id_extern).first():
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
                deal_id = auto_assign_deal(db, target_addr)
                
                nova_email = Email(
                    deal_id=deal_id,
                    from_address=clean_from,
                    to_address=clean_to,
                    assumpte=assumpte[:500],
                    cos=cos,
                    direccio=direccio,
                    llegit=(direccio == "OUT"),
                    sincronitzat=True,
                    message_id_extern=message_id_extern,
                    data_email=data_email
                )
                db.add(nova_email)
                
                # Log activity if vinculado
                if deal_id:
                    activitat = models.DealActivitat(
                        deal_id=deal_id,
                        tipus="email_rebut",
                        descripcio=f"Email rebut de {clean_from}: {assumpte}"
                    )
                    db.add(activitat)
                    
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
