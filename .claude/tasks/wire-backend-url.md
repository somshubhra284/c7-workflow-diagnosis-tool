# Task: Wire backend URL into the Gradio Space

## Goal
The Gradio Space somshubhra/c7-workflow-diagnosis (frontend) reads
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000/diagnose").
The localhost default does not work on the deployed Space. Point it at the live
FastAPI backend on Render.

## Verified
Backend: https://c7-workflow-diagnosis-tool-swqg.onrender.com
- GET /        -> {"status":"ok","message":"Workflow Diagnosis Tool API"}
- GET /health  -> {"status":"ok"}
- POST /diagnose -> real plan returned. All live.

## Task list
1. [ ] Set Space secret BACKEND_URL on somshubhra/c7-workflow-diagnosis to
       https://c7-workflow-diagnosis-tool-swqg.onrender.com/diagnose
       (full endpoint, since app.py posts to BACKEND_URL directly).
2. [ ] Confirm the Space is RUNNING / picks up the secret.
3. [ ] Document BACKEND_URL in .env.example + a README note.
4. [ ] Commit + push repo doc changes (Space secret is not in git).

## Notes
- Set as a SECRET (not a visible variable) since it is infra config.
- app.py expects the full /diagnose path, so include it in the value.

## Changes log
- Set Space SECRET BACKEND_URL = .../onrender.com/diagnose via
  huggingface_hub HfApi.add_space_secret (no `hf` CLI subcommand exists for this).
- HIT A SNAG: Space went to CONFIG_ERROR -> "Collision on variables and secrets
  names". A pre-existing PUBLIC variable BACKEND_URL already existed; adding the
  secret with the same name collides. Fixed by deleting the public variable
  (delete_space_variable), keeping only the secret. Space rebuilt automatically
  to RUNNING (error: None).
- Note: explicit restart_space 401s because the OAuth login token
  (oauth-somshubhra) lacks that scope; not needed — secret/variable writes
  auto-trigger a rebuild.
- Verified end-to-end via gradio_client: Space /diagnose endpoint -> BACKEND_URL
  secret -> Render backend -> Groq -> real plan returned.
- .env.example: documented BACKEND_URL (as a Space secret).
- README.md: added "Deployment" section (backend Render URL, frontend Space,
  BACKEND_URL secret wiring).

All tasks complete.
