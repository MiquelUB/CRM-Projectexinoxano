import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import uuid
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal
import models
from models import Email

SMTP_HOST = os.getenv("SMTP_HOST", "mail.cdmon.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SSL = str(os.getenv("SMTP_SSL", "false")).lower() == "true"
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def send_email_from_crm(to_address: str, assumpte: str, cos: str, deal_id: str = None, contacte_id: str = None) -> Email:
    tracking_token = str(uuid.uuid4()).replace('-', '')
    pixel_url = f"{BASE_URL}/tracking/{tracking_token}"
    pixel_html = f'<img src="{pixel_url}" width="1" height="1" style="display:none;" />'
    
    cos_final = cos + "\n" + pixel_html
    
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_address
    msg['Subject'] = assumpte
    
    msg.attach(MIMEText(cos_final, 'html'))
    
    server = None
    try:
        if SMTP_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            if SMTP_TLS:
                server.starttls()
        
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e
    finally:
        if server:
            try: server.quit()
            except: pass
    
    db = SessionLocal()
    try:
        nova_email = Email(
            deal_id=deal_id,
            contacte_id=contacte_id,
            from_address=SMTP_USER,
            to_address=to_address,
            assumpte=assumpte,
            cos=cos,
            direccio="OUT",
            llegit=True,
            sincronitzat=True,
            data_email=datetime.now(),
            tracking_token=tracking_token
        )
        db.add(nova_email)
        
        # Log activity
        if deal_id:
            activitat = models.DealActivitat(
                deal_id=deal_id,
                tipus="email_enviat",
                descripcio=f"Email enviat: {assumpte}"
            )
            db.add(activitat)
            
        db.commit()
        db.refresh(nova_email)
        return nova_email
    finally:
        db.close()
