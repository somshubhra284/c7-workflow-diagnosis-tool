# Task: FastAPI endpoint exposing diagnose()

## Goal
Expose the workflow diagnosis tool over HTTP. Endpoints confirmed with user:
**diagnose + evaluate + health**.

## Deps
- fastapi, uvicorn[standard] (installed: fastapi 0.138.1, uvicorn 0.49.0).
- Add both to requirements.txt.

## Task list
1. [ ] requirements.txt — add fastapi + uvicorn[standard].
2. [ ] api.py — import diagnose/evaluate from main.py (single source of truth):
       - GET  /health   -> {"status": "ok"}
       - POST /diagnose -> {workflow_description} -> {plan}
       - POST /evaluate -> {workflow_description, plan} -> score dict
       - Pydantic request models with min_length validation.
       - Wrap LLM calls; return HTTP 502 on failure.
3. [ ] README.md — add "Run the API" section (uvicorn api:app --reload, /docs).
4. [ ] Verify — start server, curl /health and /diagnose, confirm real responses.

## MVP scope
No auth, no rate limiting, no streaming. Clean endpoints + interactive /docs.

## Changes log
- requirements.txt: added fastapi==0.138.1, uvicorn[standard]==0.49.0.
- api.py: created FastAPI app importing diagnose/evaluate from main.py.
  GET /health, POST /diagnose, POST /evaluate. Pydantic models with
  min_length=10 validation; LLM failures wrapped as HTTP 502.
- README.md: added "Run the API" section with uvicorn cmd, endpoints, curl example.
- Verified (uvicorn on port 8123): /health -> {"status":"ok"}; /diagnose ->
  real Groq plan; too-short input -> 422 validation error. All passed.

All tasks complete.
