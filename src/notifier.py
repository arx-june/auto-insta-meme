# src/notifier.py

import os
import requests
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Bring in your debug flag
from config import DEBUG_MODE, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(message: str):
    """Send a message via Telegram bot with retries and safe error handling."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    # 1) Set up a session with retry policy
    session = requests.Session()
    retry_strategy = Retry(
        total=3,                # retry up to 3 times
        backoff_factor=1,       # wait [1s, 2s, 4s] between retries
        status_forcelist=[429, 502, 503, 504],
        allowed_methods=["POST"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)

    try:
        resp = session.post(url, data=payload, timeout=30)
        resp.raise_for_status()
        if DEBUG_MODE:
            print(f"[DEBUG] Telegram send OK: {resp.status_code}")
    except requests.RequestException as e:
        # Log the error but don’t crash
        if DEBUG_MODE:
            print(f"[DEBUG] Telegram send failed: {e!r}")


