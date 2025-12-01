from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.feed_engine import run_digest, capture_url, get_daily_pulse, get_feed, add_source, list_sources

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
def capture(data: CaptureRequest):
    return capture_url(data.url)


@app.get("/api/daily_pulse")
def daily_pulse():
    return get_daily_pulse()


@app.post("/api/run_digest")
def digest():
    return run_digest()


@app.post("/api/add_source")
def add_source_route(data: SourceRequest):
    add_source(data.url)
    return {"status": "added", "url": data.url}


@app.get("/api/list_sources")
def list_sources_route():
    return list_sources()
