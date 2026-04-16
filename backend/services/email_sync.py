
import os
import sys
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import re
from datetime import datetime, timedelta, timezone
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal
import models

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
    prev_email = db.query(models.Email).filter(
        or_(models.Email.from_address == email_addr, models.Email.to_address == email_addr)
    ).order_by(models.Email.data_enviament.desc()).first()
    
    if prev_email and prev_email.municipi_id:
        return str(prev_email.municipi_id)
        
    contacte = db.query(models.Contacte).filter(models.Contacte.email == email_addr).first()
    if contacte and contacte.municipi_id:
        return str(contacte.municipi_id)
            
    domain = extract_domain(email_addr)
    if domain and domain not in ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]:
        municipis = db.query(models.Municipi).all()
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

def find_sent_folder(mail):
    """Llista les carpetes i intenta trobar la de 'Enviats'"""
    try:
        status, folders = mail.list()
        if status != "OK": return "Sent"
        
        # Patrons comuns per a carpetes enviades
        patterns = [r'sent', r'enviats', r'enviados', r'envi', r'sortida']
        
        for f in folders:
            folder_info = f.decode('utf-8', errors='replace')
            # El format de mail.list() sol ser: (Attributes) "Hierarchy" FolderName
            match = re.search(r'"([^"]+)"$', folder_info)
            if not match:
                match = re.search(r' ([^ ]+)$', folder_info)
            
            if match:
                folder_name = match.group(1).replace('"', '')
                for p in patterns:
                    if re.search(p, folder_name.lower()):
                        return folder_name
    except:
        pass
    return "Sent"

def extract_email_address(full_address):
    if not full_address: return ""
    match = re.search(r'<([^>]+)>', full_address)
    if match: return match.group(1).strip().lower()
    return full_address.strip().lower()

def sync_mailbox(folder="INBOX", direccio="IN", search_criteria="UNSEEN"):
    if not IMAP_HOST or not IMAP_USER:
        logger.warning(f"IMAP settings missing, skipping sync {direccio}")
        return
        
    db = SessionLocal()
    mail = None
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) if IMAP_SSL else imaplib.IMAP4(IMAP_HOST, IMAP_PORT)
        mail.login(IMAP_USER, IMAP_PASSWORD)
        
        target_folder = folder
        if folder != "INBOX" and direccio == "OUT":
            target_folder = find_sent_folder(mail)
            # Si no trobem carpeta d'enviats, no sincronitzem OUT per evitar errors
            if target_folder == "Sent": # Fallback per defecte que sabem que falla
                 logger.warning("No sent folder found, skipping OUT sync.")
                 return
            logger.info(f"DEBUG: Found sent folder: {target_folder}")

        status, messages = mail.select(target_folder)
        if status != "OK" and not target_folder.startswith("INBOX."):
            status, messages = mail.select(f"INBOX.{target_folder}")
            if status == "OK": target_folder = f"INBOX.{target_folder}"
        
        if status != "OK":
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
                
                if message_id_extern and db.query(models.Email).filter(models.Email.message_id_extern == message_id_extern).first():
                    continue
                    
                assumpte = decode_mime_header(msg.get("Subject", ""))
                from_address = decode_mime_header(msg.get("From", ""))
                to_address = decode_mime_header(msg.get("To", ""))
                
                try:
                    data_email = parsedate_to_datetime(msg.get("Date"))
                except:
                    data_email = datetime.now(timezone.utc)
                    
                clean_from = extract_email_address(from_address)
                clean_to = extract_email_address(to_address)
                
                cos = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() in ["text/plain", "text/html"]:
                            try:
                                body = part.get_payload(decode=True)
                                if body: cos += body.decode(part.get_content_charset() or 'utf-8', errors='replace')
                            except: pass
                else:
                    try:
                        body = msg.get_payload(decode=True)
                        if body: cos = body.decode(msg.get_content_charset() or 'utf-8', errors='replace')
                    except: pass
                
                target_addr = clean_from if direccio == "IN" else clean_to
                municipi_id = auto_assign_municipi(db, target_addr)
                
                dir_unificat = "entrada" if direccio == "IN" else "sortida"
                
                email_obj = models.Email(
                    municipi_id=municipi_id,
                    from_address=clean_from,
                    to_address=clean_to,
                    assumpte=assumpte[:200],
                    cos=cos,
                    direccio=dir_unificat,
                    data_enviament=data_email,
                    message_id_extern=message_id_extern,
                    llegit=(direccio == "OUT")
                )
                db.add(email_obj)
                
                if municipi_id:
                    tipus_act = models.TipusActivitat.email_rebut if direccio == "IN" else models.TipusActivitat.email_enviat
                    activitat = models.Activitat(
                        municipi_id=municipi_id,
                        tipus_activitat=tipus_act,
                        data_activitat=data_email,
                        notes_comercial=f"Email ({direccio}) sincronitzat via IMAP"
                    )
                    db.add(activitat)
                
                db.commit()
            except Exception as e:
                logger.error(f"Error processing message {num}: {e}")
                db.rollback()
                
    except Exception as e:
        logger.error(f"Global sync error: {e}")
    finally:
        if mail: mail.logout()
        db.close()

def sync_all_emails():
    logger.info("Starting IMAP email sync...")
    sync_mailbox("INBOX", "IN", "UNSEEN")
    # Intentar sincronitzar enviats dels últims 3 dies
    date_since = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%d-%b-%Y")
    sync_mailbox("Sent", "OUT", f'SINCE "{date_since}"')
    logger.info("IMAP email sync finished.")

if __name__ == "__main__":
    sync_all_emails()
