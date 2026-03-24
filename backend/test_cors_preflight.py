import os
import sys
from fastapi.testclient import TestClient
from dotenv import load_dotenv

if os.path.exists(".env.local"):
    load_dotenv(".env.local")
else:
    load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

client = TestClient(app)

print("Making CORS request to /emails")
try:
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    }
    response = client.options("/emails", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
except Exception as e:
    print(f"CORS request failed: {e}")
    import traceback
    traceback.print_exc()
