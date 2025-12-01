#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TaylorVentureLab — Feed Engine & Automation Layer

import os
import calendar
import requests
import feedparser
import time

from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

try:
    from agent.llm_summarizer import summarize_article
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

SOURCES: List[str] = []
FEED_CACHE: List[Dict[str, Any]] = []
LAST_DIGEST: Dict[str, Any] = {}

load_dotenv()
TIME_WINDOW_HOURS = int(os.getenv("TIME_WINDOW_HOURS", 24))

@dataclass
class ArticleSummary:
    title: str
    link: str
    source: str
    published_date: str
    categories: List[str] = field(default_factory=list)
    summary: str = ""
    _raw_excerpt: Optional[str] = None

def _safe_struct_time_to_utc_dt(t: time.struct_time) -> Optional[datetime]:
    if not t:
        return None
    try:
        ts = calendar.timegm(t)
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except Exception:
        return None

def _select_largest_text_container(candidates):
    best_node = None
    best_len = 0
    for node in candidates:
        try:
            text = " ".join(p.get_text(" ", strip=True) for p in node.find_all("p")
            )
        except Exception:
            continue
    return best_node

def extract_article_text(url: str) -> str:
    try:
        r = requests.get(url, timeout=10)
    except Exception:
        return ""

    soup = BeautifulSoup(r.text, "html.parser")
    candidates = soup.find_all(["article", "section", "div"])

    best = _select_largest_text_container(candidates)
    if not best:
        return ""

    paragraphs = [p.get_text(" ", strip=True) for p in best.find_all("p")]
    return "\n".join(paragraphs)

def add_source(url: str):
    if url not in SOURCES:
        SOURCES.append(url)
    return {"status": "ok", "sources": SOURCES}

def list_sources():
    return {"sources": SOURCES}

def capture_url(url: str):
    FEED_CACHE.append({
        "url": url,
        "captured_at": datetime.utcnow().isoformat()
    })
    return {"status": "captured", "url": url}

def fetch_feed_items() -> List[Dict[str, Any]]:
    items = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=TIME_WINDOW_HOURS)

    for src in SOURCES:
        try:
            parsed = feedparser.parse(src)
            for entry in parsed.entries:
                pub_dt = (
                    _safe_struct_time_to_utc_dt(entry.get("published_parsed")) or
                    _safe_struct_time_to_utc_dt(entry.get("updated_parsed"))
                )
                if not pub_dt or pub_dt < cutoff:
                    continue

                items.append({
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "summary": entry.get("summary", ""),
                    "published": pub_dt.isoformat(),
                    "source": src
                })
        except Exception as e:
            print(f"[Feed Error] {src}: {e}")
    return items

def summarize_text(text: str) -> str:
    if OPENAI_AVAILABLE:
        try:
            return summarize_article(text)
        except Exception:
            pass
    return text[:240] + "..." if len(text) > 240 else text

def run_digest():
    items = fetch_feed_items()
    summarized_items = []
    for item in items:
        article_text = extract_article_text(item["link"])
        merged_text = article_text or item["summary"]
        summarized_items.append({
            "title": item["title"],
            "link": item["link"],
            "published": item["published"],
            "source": item["source"],
            "summary": summarize_text(merged_text)
        })

    LAST_DIGEST["generated_at"] = datetime.utcnow().isoformat()
    LAST_DIGEST["items"] = summarized_items
    return {"digest": LAST_DIGEST}

def get_daily_pulse():
    if not LAST_DIGEST:
        run_digest()
    return LAST_DIGEST

def get_feed():
    return {
        "captured": FEED_CACHE,
        "digest": LAST_DIGEST,
        "sources": SOURCES
    }
#
