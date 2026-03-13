import requests

BASE_URL = "http://localhost:8000"

def test_create_municipi():
    # 1. Login to get token
    login_data = {
        "username": "admin@projectexinoxano.cat",
        "password": "pxx_admin_2026!"
    }
    
    print("Attempting login...")
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code} - {response.text}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # 2. Create Municipi
    municipi_data = {
        "nom": "Municipi de Test Antigravity",
        "tipus": "ajuntament",
        "provincia": "Barcelona",
        "poblacio": 1000,
        "web": "https://test.cat",
        "telefon": "930000000",
        "adreca": "Carrer Major 1",
        "notes": "Test creation"
    }
    
    print("Attempting to create municipi...")
    response = requests.post(f"{BASE_URL}/municipis", json=municipi_data, headers=headers)
    
    if response.status_code == 201:
        print("SUCCESS: Municipi created successfully!")
        print(response.json())
    else:
        print(f"FAILED: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_create_municipi()
