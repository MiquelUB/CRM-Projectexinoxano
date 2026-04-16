
import os
import sys
from dotenv import load_dotenv

# Afegim el path del backend
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.email_sender import send_email_from_crm

def test_send():
    print("Iniciant prova d'enviament d'email...")
    import traceback
    try:
        destinatari = "miquel@projectexinoxano.cat" 
        assumpte = "Prova de connexió CRM PXX - Port 465"
        cos = "<h1>Hola Miquel!</h1><p>Aquest correu confirma que la configuració de ports (465) i enviament des de EasyPanel és 100% operativa.</p>"
        
        email = send_email_from_crm(
            to_address=destinatari,
            assumpte=assumpte,
            cos=cos
        )
        print(f"Email enviat correctament! ID: {email.id}")
    except Exception as e:
        print(f"ERROR EN L'ENVIAMENT:")
        traceback.print_exc()

if __name__ == "__main__":
    test_send()
