# 1) File: app/main.py
# 2) Purpose: FastAPI demo service for Data Transform exposing /healthz and /demo/example with CORS.
# 3) Why: Backend for the Option 2 demo endpoint; runs behind NGINX TLS on Oracle VM.
# 4) Related: Dockerfile, docker-compose.yml, ops/nginx/data-transform.conf, site-vividsuite-io/src/components/DemoPanel.astro

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import os
import datetime as dt

APP_NAME = "VividSuite Data Transform Demo"
APP_VERSION = "0.1.0"

# Config
allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "https://vividsuite.io,http://localhost:4321").split(",") if o.strip()]
allow_netlify_wildcard = os.getenv("ALLOW_NETLIFY_WILDCARD", "true").lower() in ("1", "true", "yes")
netlify_regex = r"^https:\/\/([a-zA-Z0-9-]+\.)*netlify\.app$"

app = FastAPI(title=APP_NAME, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=netlify_regex if allow_netlify_wildcard else None,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)

@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse({
        "service": "data-transform",
        "name": APP_NAME,
        "version": APP_VERSION,
        "endpoints": ["/healthz", "/demo/example"],
    })

@app.get("/healthz")
async def healthz() -> JSONResponse:
    return JSONResponse({
        "status": "ok",
        "service": "data-transform",
        "time": dt.datetime.utcnow().isoformat() + "Z",
    })

# Simple synthetic transform: take a sample record and produce a normalized output
SAMPLE_INPUT = {
    "id": "123",
    "name": "  Alice Johnson  ",
    "email": "Alice@example.COM",
    "tags": ["New", "customer", "BETA"],
}

def normalize(rec: dict) -> dict:
    name = rec.get("name", "").strip()
    email = rec.get("email", "").strip().lower()
    tags = [str(t).strip().lower() for t in rec.get("tags", [])]
    return {
        "id": str(rec.get("id", "")).strip(),
        "name_first": name.split(" ")[0] if name else None,
        "name_last": (name.split(" ", 1)[1] if " " in name else None),
        "email": email,
        "tags": sorted(set(tags)),
        "valid": bool(email and "@" in email),
    }

@app.get("/demo/example")
async def demo_example(request: Request) -> JSONResponse:
    normalized = normalize(SAMPLE_INPUT)
    return JSONResponse({
        "service": "data-transform",
        "message": "transform-ok",
        "input": SAMPLE_INPUT,
        "output": normalized,
    })

# For local dev: `uvicorn app.main:app --reload --port 8002`
