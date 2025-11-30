#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TaylorVentureLab — Daily Feed-Summarizing Agent

This script fetches recent items from RSS/Atom feeds, scrapes full article
content, classifies topics, generates summaries (LLM or heuristic),
and outputs a JSON + Markdown digest.

Dependencies:
- requests
- feedparser
- beautifulsoup4
- python-dotenv
- openai (optional for real summaries)
"""

import os
import re
import time
import calendar
import json
import requests
import feedparser

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Optional OpenAI summarizer
try:
    from llm_summarizer import summarize_article
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


# =========================
# 1) Configuration & Feeds
# =========================

load_dotenv()

TIME_WINDOW_HOURS = int(os.getenv("TIME_WINDOW_HOURS", 24))
SUMMARY_MODEL_NAME = os.getenv("SUMMARY_MODEL_NAME", "gpt-4o-mini")

# Output filename for the daily digest
OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME", "daily_digest.md")

# Feed registry
FEEDS: Dict[str, str] = {
    "Hootsuite Blog": "https://blog.hootsuite.com/feed/",
    "Sprout Social": "https://sproutsocial.com/insights/feed/",
}


# =========================
# 2) Data Model
# =========================

@dataclass
class ArticleSummary:
    title: str
    link: str
    source: str
    published_date: str
    categories: List[str] = field(default_factory=list)
    summary: str = ""
    _raw_excerpt: Optional[str] = None


# =========================
# 3) Utilities
# =========================

def _safe_struct_time_to_utc_dt(t: time.struct_time) -> Optional[datetime]:
    if not t:
        return None
    try:
        ts = calendar.timegm(t)
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except:
        return None


def load_config() -> Dict[str, Any]:
    load_dotenv()
    return {
        "TIME_WINDOW_HOURS": int(os.getenv("TIME_WINDOW_HOURS", TIME_WINDOW_HOURS)),
        "SUMMARY_MODEL_NAME": os.getenv("SUMMARY_MODEL_NAME", SUMMARY_MODEL_NAME),
        "OUTPUT_FILENAME": os.getenv("OUTPUT_FILENAME", OUTPUT_FILENAME),
    }


def fetch_and_filter_feed(url: str) -> List[dict]:
    print(f"-> Fetching feed: {url}")
    feed = feedparser.parse(url)

    if feed.bozo:
        print(f"   Warning: feed parser issue: {feed.bozo_exception}")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=TIME_WINDOW_HOURS)
    results = []

    for entry in feed.entries:
        pub_dt = _safe_struct_time_to_utc_dt(entry.get("published_parsed")) \
            or _safe_struct_time_to_utc_dt(entry.get("updated_parsed"))
        if not pub_dt:
            continue
        if pub_dt < cutoff:
            continue

        title = entry.get("title", "Untitled")
        link = entry.get("link", "").strip()

        raw_tags = entry.get("tags", [])
        categories = []
        for t in raw_tags or []:
            term = getattr(t, "term", None) or t.get("term") if isinstance(t, dict) else None
            if term:
                categories.append(str(term).strip())

        excerpt = (entry.get("summary") or entry.get("description") or "").strip()

        results.append({
            "title": title,
            "link": link,
            "published_date": pub_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "categories": categories,
            "feed_excerpt": excerpt,
        })

    print(f"   Found {len(results)} entries in window.")
    return results


def _select_largest_text_container(candidates):
    best_node, best_len = None, 0
    for node in candidates:
        try:
            text = " ".join(p.get_text(" ", strip=True) for p in node.find_all("p"))
            if len(text) > best_len:
