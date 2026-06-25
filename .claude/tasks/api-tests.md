# Task: Test cases for the API endpoints

## Goal
Test /health, /diagnose, /evaluate using FastAPI's TestClient WITHOUT calling the
real Groq API. Mock diagnose/evaluate at the api module boundary so tests are fast,
free, deterministic, and need no API key. Assert routing, validation, response
shape, and error handling.

## Deps
- pytest (MISSING -> install + add to requirements.txt).
- httpx (already present; required by TestClient).

## Task list
1. [ ] requirements.txt — add pytest.
2. [ ] test_api.py — TestClient(app) + monkeypatch stubbing api.diagnose / api.evaluate:
       - /health -> 200, {"status":"ok"}
       - /diagnose happy path -> 200, {"plan": ...}; mock received correct input
       - /diagnose validation -> too-short "hi" -> 422; missing field -> 422
       - /diagnose LLM failure -> mock raises -> 502 with detail
       - /evaluate happy path -> 200, score dict echoed
       - /evaluate validation -> missing plan -> 422
       - /evaluate LLM failure -> mock raises -> 502
3. [ ] Verify — pytest -v all green.

## Key choice
Mock at api.diagnose / api.evaluate (the names api.py imported) so no network /
no API key. Unit tests for the API layer, not the LLM.

## MVP scope
~8 focused tests, no CI config.

## Changes log
- requirements.txt: added pytest==9.1.1.
- test_api.py: 8 tests using TestClient(api.app) + monkeypatch on
  api.diagnose / api.evaluate. Covers /health, both happy paths (incl. input
  pass-through assertion), validation 422s (too-short, missing field, missing
  plan), and LLM-failure 502s for both endpoints. No network, no API key needed.
- Verified: `python3 -m pytest test_api.py -v` -> 8 passed in 0.31s.
- Note: one harmless StarletteDeprecationWarning about httpx/TestClient; not
  affecting results.

All tasks complete.
