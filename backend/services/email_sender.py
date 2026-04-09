import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import uuid
from datetime import datetime
import sys
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal
import models
from models import Email

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.projectexinoxano.cat")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "miquel@projectexinoxano.cat")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SSL = str(os.getenv("SMTP_SSL", "true")).lower() == "true"
SMTP_TLS = str(os.getenv("SMTP_TLS", "false")).lower() == "true"
BASE_URL = os.getenv("BASE_URL", "https://crm.projectexinoxano.cat")

print(f"[SMTP Config] Host={SMTP_HOST}, Port={SMTP_PORT}, User={SMTP_USER}, SSL={SMTP_SSL}, TLS={SMTP_TLS}")

from email.mime.base import MIMEBase
from email import encoders

def send_email_from_crm(to_address: str, assumpte: str, cos: str, deal_id: str = None, contacte_id: str = None, attachments: list = None) -> Email:
    to_address = to_address.strip()
    print(f"[send_email_from_crm] Iniciant enviament a: {to_address} | Assumpte: {assumpte}")
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
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{attachment["filename"]}"',
            )
            msg.attach(part)
    
    server = None
    try:
        # PRIMER INTENT: SEGONS CONFIGURACIÓ (Normalment SSL a 465)
        print(f"[SMTP] Primer intent: {SMTP_HOST}:{SMTP_PORT} (SSL: {SMTP_SSL}, TLS: {SMTP_TLS})")
        try:
            if SMTP_SSL:
                server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20)
            else:
                server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
                if SMTP_TLS:
                    print("[SMTP] Iniciant STARTTLS...")
                    server.starttls()
            
            print(f"[SMTP] Logging in com a {SMTP_USER}...")
            server.login(SMTP_USER, SMTP_PASSWORD)
            print("[SMTP] Enviant missatge...")
            server.send_message(msg)
            print("[SMTP] Missatge enviat correctament (Intent 1).")
        except (smtplib.SMTPConnectError, socket.timeout, ConnectionRefusedError, OSError) as e:
            print(f"[SMTP] Intent 1 ha fallat: {e}. Provant alternativa...")
            # ALTERNATIVA: Port 587 amb STARTTLS (sovint disponible quan 465 està bloquejat)
            alt_port = 587
            print(f"[SMTP] Segon intent: {SMTP_HOST}:{alt_port} (STARTTLS)")
            if server: 
                try: server.close()
                except: pass
            
            server = smtplib.SMTP(SMTP_HOST, alt_port, timeout=20)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print("[SMTP] Missatge enviat correctament en el Segon Intent (587)!")
            
    except Exception as e:
        print(f"[SMTP] ERROR FINAL EN ENVIAMENT: {e}")
        import traceback
        traceback.print_exc()
        raise e
    finally:
        if server:
            try: server.quit()
            except: pass
    
    db = SessionLocal()
    try:
        # 1. Guardar a V1 (Legacy)
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
        
        # 2. Guardar a V2 (Nova Arquitectura)
        import models_v2
        # Intentar trobar el municipi_id a partir del deal si no ve informat
        found_municipi_id = None
        if deal_id:
            old_deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
            if old_deal:
                # Buscar el MunicipiLifecycle pel nom o pel mapping si el tinguéssim
                # En aquest flux, assumim que el deal_id encara és el vell.
                # Per ara, busquem per nom del municipi original
                old_muni = db.query(models.Municipi).filter(models.Municipi.id == old_deal.municipi_id).first()
                if old_muni:
                    new_muni = db.query(models_v2.MunicipiLifecycle).filter(models_v2.MunicipiLifecycle.nom == old_muni.nom).first()
                    if new_muni:
                        found_municipi_id = new_muni.id

        if found_municipi_id:
            # Crear registre a emails_v2
            email_v2 = models_v2.EmailV2(
                municipi_id=found_municipi_id,
                contacte_id=contacte_id if contacte_id else None,
                assumpte=assumpte,
                cos=cos,
                direccio="sortida",
                tracking_token=tracking_token,
                data_enviament=datetime.now()
            )
            db.add(email_v2)
            
            # Crear activitat de timeline
            activitat_v2 = models_v2.ActivitatsMunicipi(
                municipi_id=found_municipi_id,
                contacte_id=contacte_id if contacte_id else None,
                tipus_activitat=models_v2.TipusActivitat.email_enviat,
                contingut={
                    "assumpte": assumpte,
                    "tracking_token": tracking_token,
                    "to": to_address
                },
                notes_comercial=f"Email enviat mitjançant CRM (V1 Bridge)"
            )
            db.add(activitat_v2)

        # Log activity (Legacy Deal)
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
