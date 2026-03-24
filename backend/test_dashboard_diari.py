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

print("Making request to /dashboard/diari")
try:
    response = client.get("/dashboard/diari")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:1000]}")
except Exception as e:
    print(f"Request failed: {e}")
