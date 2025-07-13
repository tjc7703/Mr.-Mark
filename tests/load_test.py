import requests
import time

URL = "http://localhost:8000/health"

for i in range(100):
    try:
        r = requests.get(URL, timeout=2)
        print(f"{i}: {r.status_code} {r.json()}")
    except Exception as e:
        print(f"{i}: ERROR {e}")
    time.sleep(0.1) 