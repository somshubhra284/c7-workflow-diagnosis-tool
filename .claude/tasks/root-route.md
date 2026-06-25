# Task: Add root `/` route to api.py

## Goal
Add a root route so GET / returns a friendly status/message (useful as a
landing/health check at the API root).

## Task list
1. [ ] api.py — add @app.get("/") returning
       {"status": "ok", "message": "Workflow Diagnosis Tool API"},
       placed right after the /health endpoint.
2. [ ] test_api.py — add test_root_returns_message asserting 200 + the body.
3. [ ] Verify — pytest (unit) green.
4. [ ] Commit + push (this task file included per the commit rule).

## MVP scope
The route as specified by the user + a matching unit test. No other changes.

## Changes log
- api.py: added @app.get("/") root route after /health, returns
  {"status": "ok", "message": "Workflow Diagnosis Tool API"}.
- test_api.py: added test_root_returns_message (200 + exact body).
- Verified: pytest -> 9 passed, 1 deselected.

All tasks complete.
