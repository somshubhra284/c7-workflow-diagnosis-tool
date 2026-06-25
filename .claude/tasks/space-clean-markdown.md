# Task: Fix Space app.py to return clean Markdown

## Problem
The Gradio Space returns response.text (the whole JSON body), so the chat shows
literal {"plan":"## Workflow Summary\n..."} with escaped newlines instead of
rendered Markdown.

## Fix
In the Space's app.py `diagnose()`, parse the JSON and return data["plan"] so
Gradio renders it as Markdown. Keep a safe fallback if "plan" is missing or the
body is not JSON.

## Task list
1. [ ] Edit /tmp/c7-space/app.py: return response.json().get("plan", response.text)
       wrapped in try/except for non-JSON; keep the existing RequestException
       handling.
2. [ ] Upload app.py to somshubhra/c7-workflow-diagnosis (repo-type space) via
       huggingface_hub upload_file. This auto-triggers a rebuild.
3. [ ] Wait for Space RUNNING, then re-test in the browser; confirm clean
       Markdown (no raw JSON).
4. [ ] Save a copy of the updated app.py in this repo (e.g. space/app.py) so the
       Space source is version-controlled here too.
5. [ ] Commit + push (task file + space/app.py copy) per the commit rule.

## Notes
- Space secret BACKEND_URL stays as-is (already wired). No secret changes.
- Outward-facing change to the live Space -> needs approval before upload.

## Changes log
- space/app.py: created in-repo (version-controlled Space source). diagnose()
  now returns response.json().get("plan", response.text) with a ValueError
  fallback for non-JSON; existing RequestException handling kept.
- Uploaded app.py to somshubhra/c7-workflow-diagnosis via HfApi.upload_file
  (commit "Return clean Markdown plan instead of raw JSON body"). Space rebuilt
  to RUNNING, error: None.
- Re-tested in the browser: response now renders as real Markdown (h2 headings +
  bullet lists), no raw {"plan":...} JSON or escaped \n. Confirmed via a11y tree.
- .gitignore: added .playwright-mcp/ and *.png (browser test artifacts).

All tasks complete.
