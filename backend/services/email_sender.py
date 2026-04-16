import smtplib
import socket
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import uuid
from datetime import datetime, timezone
import sys
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal
import models

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.projectexinoxano.cat")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "miquel@projectexinoxano.cat")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SSL = str(os.getenv("SMTP_SSL", "true")).lower() == "true"
SMTP_TLS = str(os.getenv("SMTP_TLS", "false")).lower() == "true"
BASE_URL = os.getenv("BASE_URL", "https://crmpxx-crm-backend.80opze.easypanel.host")

from email.mime.base import MIMEBase
from email import encoders

def send_email_from_crm(to_address: str, assumpte: str, cos: str, municipi_id: str = None, contacte_id: str = None, attachments: list = None) -> models.Email:
    to_address = to_address.strip()
    tracking_token = str(uuid.uuid4()).replace('-', '')
    pixel_url = f"{BASE_URL}/tracking/{tracking_token}"
    pixel_html = f'<img src="{pixel_url}" width="1" height="1" style="display:none;" />'
    
    cos_final = cos + "\n" + pixel_html
    
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_address
    msg['Subject'] = assumpte
    msg.attach(MIMEText(cos_final, 'html'))
    
    if attachments:
        for attachment in attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment['content'])
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment["filename"]}"')
            msg.attach(part)
    
    server = None
    try:
        print(f"DEBUG SEND: Connecting to {SMTP_HOST}:{SMTP_PORT} (SSL: {SMTP_SSL}, TLS: {SMTP_TLS})")
        if SMTP_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
            if SMTP_TLS:
                print("DEBUG SEND: Starting TLS sequence...")
                server.starttls()
        
        print(f"DEBUG SEND: Attempting login as {SMTP_USER}...")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("DEBUG SEND: Login successful. Sending message...")
        server.send_message(msg)
        server.quit()
        print("DEBUG SEND: Email sent successfully and connection closed.")
    except Exception as e:
        logger.error(f"Error SMTP: {e}")
        # Secondary attempt
        try:
            if server: server.close()
            server = smtplib.SMTP(SMTP_HOST, 587, timeout=20)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        except Exception as e2:
            raise e2
    finally:
        if server: server.quit()
    
    db = SessionLocal()
    try:
        nou_email = models.Email(
            municipi_id=municipi_id,
            contacte_id=contacte_id,
            from_address=SMTP_USER,
            to_address=to_address,
            assumpte=assumpte,
            cos=cos,
            direccio="sortida",
            llegit=True,
            data_enviament=datetime.now(timezone.utc),
            tracking_token=tracking_token
        )
        db.add(nou_email)
        
        if municipi_id:
            activitat = models.Activitat(
                municipi_id=municipi_id,
                contacte_id=contacte_id,
                tipus_activitat=models.TipusActivitat.email_enviat,
                notes_comercial=f"Email enviat: {assumpte}"
            )
            db.add(activitat)
            
        db.commit()
        db.refresh(nou_email)
        return nou_email
    finally:
        db.close()
