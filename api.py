#modules necessary for running the fastapi
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
import uvicorn

#recommendation function from recommender.py
from recommender import get_top_assessments


# Defining FastAPI app

app = FastAPI(
    title="SHL Assessment Recommender",
    description="Hybrid BM25 + Embedding Recommender API",
)

# Serve static files from /static/
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set template directory
templates = Jinja2Templates(directory="templates")


class RecommendRequest(BaseModel):
    query: str
    max_duration: Optional[int] = None
    remote_testing: Optional[bool] = None
    adaptive_irt: Optional[bool] = None

class URLRequest(BaseModel):
    url: HttpUrl

class JobDescriptionRequest(BaseModel):
    url: str

# Routes

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    """Serve the main UI HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "OK"}


@app.post("/recommend")
async def recommend(req: RecommendRequest) -> Dict[str, Any]:
    """
    Recommend SHL assessments based on query and optional filters.
    """
    #Retrieve top candidates
    raw = get_top_assessments(req.query, K=50, N=10)

    #Filter based on optional fields
    filtered = []
    for r in raw:
        if req.max_duration is not None and r.get("duration") is not None:
            if r["duration"] > req.max_duration:
                continue
        if req.remote_testing and not r.get("remote_testing", False):
            continue
        if req.adaptive_irt and not r.get("adaptive_irt", False):
            continue
        filtered.append(r)

    return {"recommendations": filtered}


# Running with Uvicorn

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)
