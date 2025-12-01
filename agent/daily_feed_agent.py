import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Any

# In-memory storage for simplicity (you can swap to DB later)
SOURCES: List[str] = []
FEED_CACHE: List[Dict[str, Any]] = []
LAST_DIGEST: Dict[str, Any] = {}


def add_source(url: str):
    if url not in SOURCES:
        SOURCES.append(url)
    return {"status": "ok", "sources": SOURCES}


def list_sources():
    return {"sources": SOURCES}


def capture_url(url: str):
    """Store or queue a URL from the extension for processing."""
    FEED_CACHE.append({
        "url": url,
        "captured_at": datetime.utcnow().isoformat()
    })
    return {"status": "captured", "url": url}


def fetch_feed_items() -> List[Dict[str, Any]]:
    """Fetch items from all RSS/Atom sources."""
    items = []
    for src in SOURCES:
        try:
            parsed = feedparser.parse(src)
            for entry in parsed.entries:
                items.append({
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "summary": entry.get("summary", ""),
                    "published": entry.get("published", "")
                })
        except Exception as e:
            print(f"Error loading feed {src}: {e}")
    return items


def summarize_text(text: str) -> str:
    """Mock summarizer (LLM integration later)."""
    if len(text) > 240:
        return text[:240] + "..."
    return text


def run_digest():
    """Build a digest of all sources and recent cached items."""
    items = fetch_feed_items()

    summarized = []
    for item in items:
        summarized.append({
            "title": item["title"],
            "link": item["link"],
            "summary": summarize_text(item["summary"])
        })

    LAST_DIGEST["generated_at"] = datetime.utcnow().isoformat()
    LAST_DIGEST["items"] = summarized

    return {"digest": LAST_DIGEST}


def get_daily_pulse():
    """Return the latest digest or force-generate one."""
    if not LAST_DIGEST:
        run_digest()
    return LAST_DIGEST


def get_feed():
    """Return the local feed (captured URLs + summaries)."""
    return {
        "captured": FEED_CACHE,
        "digest": LAST_DIGEST
    }
