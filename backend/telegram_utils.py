# telegram_utils.py

import os
import logging
import requests

# Load from env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("🚨 Telegram bot token or chat ID is missing.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info("✅ Telegram message sent.")
            return True
        else:
            logging.warning(f"⚠️ Failed to send Telegram message: {response.text}")
            return False
    except Exception as e:
        logging.error(f"❌ Telegram exception: {e}")
        return False
