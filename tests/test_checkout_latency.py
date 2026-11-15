import os
import time
import urllib.request

BASE_URL = os.getenv("INCIDENTHUB_URL", "http://localhost:8000")

def test_checkout_summary_responds_under_350ms():
    start = time.perf_counter()
    with urllib.request.urlopen(f"{BASE_URL}/api/checkout/summary", timeout=5) as response:
        assert response.status == 200
    elapsed = time.perf_counter() - start
    assert elapsed < 0.35, f"checkout summary took {elapsed:.2f}s; expected < 0.35s"
