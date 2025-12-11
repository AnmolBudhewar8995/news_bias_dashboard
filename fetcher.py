# src/fetcher.py
import feedparser, time, yaml
from newspaper import Article
from pathlib import Path
from datetime import datetime
from src.db import init_db, save_article_if_new
from tqdm import tqdm

FEEDS_PATH = Path("feeds.yaml")

def load_feeds():
    import yaml
    cfg = yaml.safe_load(FEEDS_PATH.read_text())
    return cfg.get("feeds", [])

def fetch_and_store():
    init_db()
    feeds = load_feeds()
    for f in feeds:
        name = f.get("name")
        url = f.get("url")
        print("Fetching feed:", name, url)
        feed = feedparser.parse(url)
        for entry in tqdm(feed.entries):
            link = entry.get("link")
            title = entry.get("title", "")
            pub = entry.get("published", entry.get("published_parsed", None))
            pub_dt = None
            if pub:
                try:
                    pub_dt = datetime(*entry.published_parsed[:6])
                except Exception:
                    pub_dt = None
            # extract article content via newspaper3k
            try:
                art = Article(link, fetch_images=False)
                art.download()
                art.parse()
                text = art.text
                authors = art.authors
            except Exception as e:
                print("Article fetch failed:", e)
                continue
            meta = {
                "source": name,
                "url": link,
                "title": title,
                "published": pub_dt.isoformat() if pub_dt else None,
                "authors": ",".join(authors) if authors else None
            }
            # store to DB if new
            save_article_if_new(url=link, title=title, source=name, published=pub_dt, text=text)
    print("Done fetching feeds.")
