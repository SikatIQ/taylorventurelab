# TaylorVentureLab — AI Feed Automation Suite

A modular, AI-enhanced feed-intelligence system designed to power the TaylorVentureLab 
ecosystem. This suite automates the collection, processing, summarization, and 
presentation of high-value content across social, marketing, and AI strategy domains.

Built for rapid insight extraction, daily pulse monitoring, and hands-free content curation.

---

## 🚀 Components

### **1. Python Agent (`/agent`)**
- Collects RSS/Atom feeds  
- Scrapes full article content  
- Classifies topics and themes  
- Generates summaries (mocked now, AI-ready)  
- Outputs:
  - Markdown digest
  - JSON feed for the extension (via future API server)

Run manually or via macOS launcher.

---

### **2. Browser Extension (`/extension`)**
A lightweight MV3 extension for Atlas/Chrome that shows your curated feed directly in the browser.

- Fetches your feed endpoint (local or remote)  
- Displays summaries, timestamps, and sources  
- Uses a dark UI optimized for scanning  
- Refresh button included  
- Designed to integrate seamlessly with OpenAI Atlas workflows

Load via *Load Unpacked* in Developer Mode.

---

### **3. Desktop Launcher (`/desktop`)**
Simple macOS launcher script:

- Creates virtual environment automatically  
- Installs dependencies  
- Executes agent  
- Ideal for Mac mini or laptop usage  
- Can be wrapped into a `.app` for dock-based execution

---

### **4. Documentation (`/docs`)**
- `ARCHITECTURE.md` — full system design  
- `SETUP.md` — installation and development guide  

Clear, modular, scalable.

---

## 📁 Project Structure
taylorventurelab/
│
├── agent/
│ ├── daily_feed_agent.py
│ ├── requirements.txt
│ ├── .env.example
│
├── extension/
│ ├── manifest.json
│ ├── popup.html
│ └── src/
│ ├── popup.js
│ └── background.js
│
├── desktop/
│ └── run_agent.sh
│
└── docs/
├── ARCHITECTURE.md
└── SETUP.md

---

## 🔥 Roadmap (Massive Expansion Potential)

### Short-Term
- Add FastAPI server to serve `/feed` endpoint  
- Integrate Instagram Graph API  
- Add TikTok pipeline  
- Enhance topic classification with embeddings  
- Add Notion/Telegram/Slack publishing automation  
- Add “Pulse Page” auto-generation  

### Mid-Term
- Build cloud deployment for 24/7 ingestion  
- Multi-source clustering + AI cross-analysis  
- Custom dashboards (Pulse, Signals, Trends)  
- Automation with n8n or Zapier  

### Long-Term
- Full Intelligence Platform grounding TaylorVentureLab ecosystem  
- Cross-vertical trend engine  
- Content strategy AI co-pilots  
- Enterprise-grade feed orchestration  

---

## 🧩 Contributing

Internal project for TaylorVentureLab.  
PRs accepted from authorized contributors.

Branch you’re working on right now:  
**`init/tvl-system`**

---

## ⚡ Author

Built by **The Sikat Agency** for **TaylorVentureLab**  
Strategic direction by Christopher Taylor.

---

## ⭐ License

Private — All Rights Reserved.

