# TaylorVentureLab — AI Feed Automation Suite
Architecture Overview

This project is structured into four core components that work together to deliver
a fully automated content-intelligence and feed-curation system.

---

## 1. Agent (Python)

Location: `/agent`

The agent performs:
- RSS/Atom feed collection  
- Article scraping (BeautifulSoup)  
- Heuristic/topic classification  
- Summary generation (mocked today, can be connected to OpenAI later)  
- Feed output generation:  
  - Markdown digest (`daily_digest.md`)  
  - JSON API output (to support the extension)

Dependencies defined in `agent/requirements.txt`.

The agent is runnable manually or via automation on macOS (see `/desktop` launcher).

---

## 2. Browser Extension (Atlas/Chrome, MV3)

Location: `/extension`

Purpose:
- Display live curated feed from the agent  
- Fetches from configurable endpoint (default: `http://localhost:8000/feed`)  
- Renders articles with metadata and summaries  
- Refresh control + future features (filtering, search, tagging)

Files:
- `manifest.json` — MV3 manifest  
- `popup.html` — UI shell  
- `src/popup.js` — fetch/feed rendering  
- `src/background.js` — service worker placeholder  

The extension is intended for use inside OpenAI Atlas Browser or any Chromium-based browser in developer mode.

---

## 3. macOS Desktop Launcher

Location: `/desktop/run_agent.sh`

Purpose:
- Quick local execution of the agent  
- Creates virtual environment if missing  
- Installs dependencies  
- Runs `agent/daily_feed_agent.py`

This script can be wrapped into an Automator `.app` for double-click execution on a Mac mini or laptop.

---

## 4. Documentation

Location: `/docs`

Includes:
- `ARCHITECTURE.md` (this file)  
- `SETUP.md` — step-by-step installation and local execution instructions

---

## 5. Root README

Provides:
- High-level project explanation  
- Structure overview  
- Setup pointers  
- Contribution workflow  

---

## System Flow Summary

