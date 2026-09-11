import json
import logging
import os
import random
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone


TARGET_URL = os.getenv("TARGET_URL", "http://api-service:5000")
INTERVAL_SECONDS = float(os.getenv("INTERVAL_SECONDS", "2"))
SCENARIOS = ["healthy", "slow", "error"]
WEIGHTS = [75, 15, 10]

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("three-tier-loadgen")


def log(level, message, **fields):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level.upper(),
        "service": "three-tier-loadgen",
        "message": message,
        **fields,
    }
    getattr(logger, level)(json.dumps(payload))


def send_request():
    scenario = random.choices(SCENARIOS, weights=WEIGHTS, k=1)[0]
    request_id = str(uuid.uuid4())
    url = f"{TARGET_URL}/simulate/{scenario}"
    outgoing_request = urllib.request.Request(url, headers={"X-Request-ID": request_id})
    started_at = time.perf_counter()
    try:
        with urllib.request.urlopen(outgoing_request, timeout=10) as response:
            status_code = response.status
    except urllib.error.HTTPError as error:
        status_code = error.code
    except Exception as error:
        log("error", "Traffic generation failed", request_id=request_id, error=str(error))
        return

    log(
        "info",
        "Simulated request sent",
        request_id=request_id,
        scenario=scenario,
        status_code=status_code,
        duration_ms=round((time.perf_counter() - started_at) * 1000, 2),
    )


if __name__ == "__main__":
    log("info", "Traffic generator started", target=TARGET_URL, interval=INTERVAL_SECONDS)
    while True:
        send_request()
        time.sleep(INTERVAL_SECONDS)
