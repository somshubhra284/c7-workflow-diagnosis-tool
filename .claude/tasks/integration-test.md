# Task: Real end-to-end integration test (hits Groq)

## Goal
One opt-in test exercising the full stack — HTTP -> api -> main.diagnose -> real
Groq — with NO mocking. Marked @pytest.mark.integration so it is skipped by
default and only runs when explicitly requested.

## Task list
1. [ ] pytest.ini — register the `integration` marker; set
       addopts = -m "not integration" so default `pytest` EXCLUDES integration
       tests. The 8 unit tests keep running offline.
2. [ ] test_api.py — append one test:
       - @pytest.mark.integration
       - skip (not fail) if GROQ_API_KEY missing, with a clear message
       - POST /diagnose with a real workflow via TestClient
       - assert 200, non-empty plan string, and contains expected section
         headers (## Workflow Summary, ## Best First Automation) -> proves the
         real LLM round-trip produced structured output
3. [ ] README.md — note: `pytest` = unit only; `pytest -m integration` = live
       Groq test (needs GROQ_API_KEY + network).
4. [ ] Verify — `pytest` (8 pass, integration deselected) and
       `pytest -m integration` (1 real call passes).

## Key choices
- Default run excludes integration -> fast/free/offline normal runs; opt in with
  -m integration.
- Skip (not fail) when no API key -> safe on machines/CI without creds.
- Assert on structure (section headers), not exact wording -> robust to LLM
  nondeterminism.

## MVP scope
One integration test, /diagnose only.

## Changes log
- pytest.ini: created. addopts = -m "not integration" (default excludes
  integration); registered `integration` marker.
- test_api.py: added `import os` and test_diagnose_end_to_end_real_groq
  (@pytest.mark.integration). Skips if GROQ_API_KEY missing. POSTs a real
  workflow to /diagnose, asserts 200 + non-empty plan + "## Workflow Summary"
  and "## Best First Automation" headers present.
- README.md: added "Tests" section documenting pytest vs pytest -m integration.
- Verified:
  - `pytest` -> 8 passed, 1 deselected, 0.31s (offline).
  - `pytest -m integration` -> 1 passed, 8 deselected, 1.34s (real Groq call).

All tasks complete.
