# main.py

import logging
import json
import os
from rss_reader import fetch_rss_articles
from ai_utils import get_best_summary
from telegram_utils import send_telegram_message

# Optional: Set logging level (DEBUG, INFO, WARNING, ERROR)
logging.basicConfig(level=logging.INFO)

LOG_FILE = "../frontend/log.json"  # <- where frontend reads from

def format_message(article: dict, summary: str) -> str:
    return (
        f"📰 <b>{article['title']}</b>\n"
        f"🧠 <b>Summary:</b> {summary}\n"
        f"🔗 <a href='{article['link']}'>Read More</a>\n"
        f"📅 <i>{article['published']}</i>"
    )

def run_bot():
    logging.info("🤖 Silver News Bot is running...")
    articles = fetch_rss_articles()

    if not articles:
        logging.info("📭 No new relevant articles found.")
        return

    # Load existing log data (if exists)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    else:
        log_data = []

    for article in articles:
        summary = get_best_summary(article['summary'] or article['title'])
        message = format_message(article, summary)
        send_telegram_message(message)

        # Append to log
        log_data.append({
            "title": article['title'],
            "summary": summary,
            "link": article['link'],
            "published": article['published']
        })

    # Save only last 50 entries to keep log clean
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data[-50:], f, indent=2)

if __name__ == "__main__":
    run_bot()
