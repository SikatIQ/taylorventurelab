from fastapi import FastAPI
from pydantic import BaseModel

# Import the functions from your feed engine
from agent.daily_feed_agent import (
    run_digest,
    get_feed,
    get_daily_pulse,
    add_source,
    list_sources,
    capture_url,
)

app = FastAPI(title="TaylorVentureLab Feed API", version="0.1.0")

class CaptureRequest(BaseModel):
    url: str

class SourceRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"message": "TaylorVentureLab API running"}

@app.get("/feed")
def feed():
    return get_feed()

@app.post("/api/capture")
def capture(req: CaptureRequest):
    return capture_url(req.url)

@app.get("/api/daily_pulse")
def daily_pulse():
    return get_daily_pulse()

@app.post("/api/run_digest")
def digest():
    return run_digest()

@app.post("/api/add_source")
def add_source_route(req: SourceRequest):
    return add_source(req.url)

@app.get("/api/list_sources")
def list_sources_route():
    return list_sources()
