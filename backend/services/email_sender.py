
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import uuid
from datetime import datetime, timezone
import sys
from dotenv import load_dotenv

load_dotenv()

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
BASE_URL = os.getenv("BASE_URL", "https://crm.projectexinoxano.cat")

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
        if SMTP_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
            if SMTP_TLS: server.starttls()
        
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
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
