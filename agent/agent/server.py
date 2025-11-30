from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="TaylorVentureLab Feed API")

# Allow your browser extension to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/feed")
def get_feed():
    """
    Returns the latest processed feed.json file created by the agent.
    """
    if not os.path.exists("feed.json"):
        raise HTTPException(status_code=404, detail="feed.json not found. Run the agent first.")

    try:
        with open("feed.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading feed.json: {e}")


@app.get("/")
def root():
    return {"status": "ok", "message": "TaylorVentureLab Feed API running"}
