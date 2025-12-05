# TaylorVentureLab — AI Feed Automation Suite  
Architecture Overview

This project is structured into four core components that work together to deliver
a fully automated content-intelligence and feed-curation system.

---

## 1. Agent (Python)

**Location:** `/agent`

The agent performs:

- RSS/Atom feed collection  
- Article scraping using BeautifulSoup  
- Heuristic topic classification  
- Summary generation (mocked today, easily upgraded to OpenAI)  
- Output generation:
  - Markdown digest (`daily_digest.md`)
  - JSON feed for browser extension consumption

**Key design goals:**

- Modular and customizable  
- Easy to schedule (cron/launchd/macOS App)  
- Expandable to Instagram, TikTok, custom APIs, and proprietary sources  
- Outputs structured data usable by the browser extension and automation tools

Dependencies live in `agent/requirements.txt`.

---

## 2. Browser Extension (Atlas/Chrome, Manifest V3)

**Location:** `/extension`

**Purpose:** Expose your curated feed directly inside the browser, integrated with your workflow  
(especially within OpenAI’s Atlas side panel).

Extension responsibilities:

- Pull latest feed from a configurable HTTP endpoint  
- Render summaries, metadata, and categories  
- Refresh button for real-time updates  
- Lightweight UI optimized for fast scanning

**Files:**

- `manifest.json` — MV3 manifest  
- `popup.html` — UI layout  
- `src/popup.js` — Feed fetching and rendering logic  
- `src/background.js` — MV3 service worker placeholder  

This extension works in:

- Atlas Browser  
- Chrome  
- Edge  
- Brave  
- Any Chromium-based browser

Load via “Load Unpacked” in Developer Mode.

---

## 3. macOS Desktop Launcher

**Location:** `/desktop/run_agent.sh`

**Purpose:**  
Enable one-click agent execution on a Mac mini, laptop, or server.

What it does:

1. Creates a Python virtual environment (`.venv`) if missing  
2. Installs dependencies from `agent/requirements.txt`  
3. Runs `agent/daily_feed_agent.py`  
4. Produces a new digest and/or feed JSON

This script can be wrapped into a macOS Automator App for true desktop app behavior.

---

## 4. Documentation

**Location:** `/docs`

Provides:

- **ARCHITECTURE.md** (this file)  
- **SETUP.md** — Installation & local development instructions  
- Additional documentation as new modules are added (API servers, webhooks, n8n automation, etc.)

---

## 5. Root README

Contains:

- High-level overview of the entire suite  
- How pieces fit together  
- How to install, run, and debug  
- How to contribute and extend

---

## System Flow Summary

```text
[ Python Agent ]
        ↓
Crawls feeds, scrapes articles,
summarizes, classifies content
        ↓
Generates Markdown & JSON feed
        ↓
[ Local or Remote Feed Endpoint ]
        ↓
[ Browser Extension Popup ]
Displays curated content feed
        ↓
[ User Experience ]
Daily insights, content strategy,
trend monitoring, automation inputs

Future Enhancements (Roadmap)

FastAPI/Flask runtime to serve real-time JSON feeds

Add Instagram Graph API ingestion

Add TikTok data ingestion (via backend)

Add Notion/Telegram/Slack posting automation

Scheduled run orchestrator

Optional Docker-based deployment

Multi-source topic clustering + AI embeddings

Smart feed ranking + priority scoring

Auto content generation for TaylorVentureLab Pulse Page

This document serves as the foundation for understanding how the suite is organized,
how the components interact, and how the system scales into the full TaylorVentureLab vision.

