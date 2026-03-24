import os
import sys
from dotenv import load_dotenv

# Add backend to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

load_dotenv("backend/.env")

from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
import models

def get_valid_token():
    db = SessionLocal()
    try:
        # Find a user or similar
        user = db.query(models.Usuari).first()
        if not user:
            print("No users in database for token.")
            return None
        
        # Generating token (We can use auth.create_access_token)
        from auth import create_access_token
        access_token = create_access_token(data={"sub": str(user.id)})
        return access_token
    finally:
        db.close()

def test_endpoint():
    client = TestClient(app)
    token = get_valid_token()
    if not token:
         print("Could not obtain token.")
         return

    db = SessionLocal()
    municipi = db.query(models.Municipi).first()
    db.close()
    
    if not municipi:
         print("No municipi found.")
         return

    print("Submitting POST /contactes...")
    payload = {
        "nom": "Test User From client",
        "carrec": "Developer",
        "email": "testclient@example.com",
        "telefon": "123456789",
        "municipi_id": str(municipi.id)
    }

    try:
        response = client.post("/contactes", json=payload, headers={"Authorization": f"Bearer {token}"})
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
    except Exception as e:
        import traceback
        with open("traceback.txt", "w") as f:
            traceback.print_exc(file=f)
        print("Exception written to traceback.txt")

if __name__ == "__main__":
    test_endpoint()
