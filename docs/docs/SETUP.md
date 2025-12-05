# TaylorVentureLab — Setup Guide  
Complete installation & local development instructions.

This document walks you through preparing the Python agent, the desktop launcher,
and the browser extension for local use in your workflow.

---

# 1. Clone the repository

If you haven't yet cloned the project:

```bash
git clone https://github.com/SikatIQ/taylorventurelab.git
cd taylorventurelab
git checkout init/tvl-system
python3 -m venv .venv
source .venv/bin/activate
pip install -r agent/requirements.txt
cp agent/.env.example agent/.env
Edit agent/.env and fill in values:

OPENAI_API_KEY — optional for now

SLACK_WEBHOOK_URL — optional

TIME_WINDOW_HOURS

SUMMARY_MODEL_NAME

OUTPUT_FILENAME
Run the agent manually
python agent/daily_feed_agent.py
This creates output files such as:

daily_digest.md

Feed JSON (coming soon once API server is added)

3. macOS Desktop Launcher

The desktop launcher lets you run the agent without touching the terminal.

Mark it executable:
chmod +x desktop/run_agent.sh
./desktop/run_agent.sh
This will:

Create .venv if missing

Install dependencies

Execute the agent

OPTIONAL: Build a macOS App

Open Automator

Choose Application

Add “Run Shell Script”

Paste:
cd "/path/to/taylorventurelab"
./desktop/run_agent.sh
Save as TaylorVentureLab Agent.app

Drag it to your Dock

4. Browser Extension (Atlas/Chrome)
Load the extension in developer mode

Open Chrome or Atlas Browser

Go to:
chrome://extensions/
Enable Developer mode

Click Load unpacked

Select the folder:
taylorventurelab/extension
Configure the feed endpoint

Open the extension popup → It will use:
http://localhost:8000/feed
once the FastAPI server is added (next steps), the extension will show live results.
Project Structure Reference
taylorventurelab/
│
├── agent/
│   ├── daily_feed_agent.py
│   ├── requirements.txt
│   └── .env.example
│
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   └── src/
│       ├── popup.js
│       └── background.js
│
├── desktop/
│   └── run_agent.sh
│
└── docs/
    ├── ARCHITECTURE.md
    └── SETUP.md
