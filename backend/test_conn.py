import http.client
import json

def test_fetch():
    print("Testing connection to localhost:8000/auth/login")
    conn = http.client.HTTPConnection("localhost", 8000)
    payload = "username=admin%40projectexinoxano.cat&password=pxx_admin_2026!"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        conn.request("POST", "/auth/login", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Status: {res.status}")
        print(f"Body: {data.decode()}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_fetch()
