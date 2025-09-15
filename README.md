# VividSuite — demo-data-transform

FastAPI demo service for the Data Transform offering. Exposes /healthz and /demo/example with CORS. Containerized for deployment behind NGINX on an Oracle Free Tier VM.

## Quick start (local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
# Visit http://localhost:8002/healthz
```

## Docker

```bash
docker compose up --build -d
# Service on http://localhost:8002
```

## Configuration

- PORT (default 8002)
- ALLOWED_ORIGINS (comma-separated list)
- ALLOW_NETLIFY_WILDCARD (true/false; allows https://*.netlify.app)

See [.env.example](.env.example) for defaults.

## Endpoints

- GET /healthz — simple health probe
- GET /demo/example — returns synthetic input and normalized output

## NGINX vhost (example)

See [ops/nginx/data-transform.conf](ops/nginx/data-transform.conf) for a sample reverse proxy config (TLS via Let\'s Encrypt).
