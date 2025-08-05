# main.py

import logging
from rss_reader import fetch_rss_articles
from ai_utils import get_best_summary
from telegram_utils import send_telegram_message

# Optional: Set logging level (DEBUG, INFO, WARNING, ERROR)
logging.basicConfig(level=logging.INFO)

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

    for article in articles:
        summary = get_best_summary(article['summary'] or article['title'])
        message = format_message(article, summary)
        send_telegram_message(message)

if __name__ == "__main__":
    run_bot()
