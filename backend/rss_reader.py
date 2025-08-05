# rss_reader.py

import feedparser
import datetime
import hashlib

# Keywords we care about
KEYWORDS = ["silver", "mcx", "comex", "bullion", "usd", "fed", "interest rate", "precious metal"]

# RSS Feed URLs (you can add more later)
RSS_FEEDS = [
    "https://economictimes.indiatimes.com/rss/commodities/rssfeedstopstories.cms",
    "https://www.reuters.com/rssFeed/commoditiesNews",
    "https://www.kitco.com/rss/news/"
]

# Memory to track seen articles (this resets every run for now)
SEEN_HASHES = set()

def clean_title(title: str) -> str:
    return title.strip().lower()

def hash_article(title: str, link: str) -> str:
    return hashlib.sha256(f"{title}{link}".encode()).hexdigest()

def is_relevant(title: str, summary: str) -> bool:
    text = f"{title} {summary}".lower()
    return any(keyword in text for keyword in KEYWORDS)

def fetch_rss_articles():
    results = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = clean_title(entry.title)
            summary = entry.get("summary", "")
            link = entry.link

            if not is_relevant(title, summary):
                continue

            article_hash = hash_article(title, link)
            if article_hash in SEEN_HASHES:
                continue  # Already processed

            SEEN_HASHES.add(article_hash)

            results.append({
                "title": title.title(),
                "summary": summary.strip(),
                "link": link,
                "published": entry.get("published", str(datetime.datetime.utcnow()))
            })

    return results
