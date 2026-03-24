import urllib.request
import time

BASE_URL = "http://127.0.0.1:8000"

endpoints = [
    "/deals/kpis",
    "/alertes",
    "/emails/stats/obertures",
    "/tasques?estat=pendent",
    "/dashboard/diari"
]

print("TESTING BACKEND ENDPOINTS:")
for ep in endpoints:
    start = time.time()
    try:
        url = f"{BASE_URL}{ep}"
        with urllib.request.urlopen(url, timeout=5) as f:
            status = f.status
            f.read()
        elapsed = time.time() - start
        print(f"[{status}] {ep} -> {elapsed:.3f}s")
    except Exception as e:
        elapsed = time.time() - start
        print(f"[FAIL] {ep} -> {elapsed:.3f}s | {type(e).__name__}")
print("Done.")
