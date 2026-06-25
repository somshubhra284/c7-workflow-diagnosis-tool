# Workflow Diagnosis Tool

Turn an analyst's plain-English workflow description into an actionable
**diagnosis plan** that identifies the single best *first* automation to build.

Powered by **Groq** (`llama-3.1-8b-instant`).

## Deployment

- **Backend** (this FastAPI app) is deployed on Render:
  `https://c7-workflow-diagnosis-tool-swqg.onrender.com`
- **Frontend** is a Gradio Space:
  [`somshubhra/c7-workflow-diagnosis`](https://huggingface.co/spaces/somshubhra/c7-workflow-diagnosis).
  The Space POSTs workflow descriptions to the backend, reading the endpoint from
  a `BACKEND_URL` **secret** set on the Space
  (`https://c7-workflow-diagnosis-tool-swqg.onrender.com/diagnose`).

## How it works

`diagnose(workflow_description)` sends the description to the LLM with an
"automation diagnosis coach" prompt. The model ranks automation opportunities by
frequency and low complexity, then returns a Markdown plan with these sections:

1. Workflow Summary
2. Automation Opportunities (ranked)
3. Best First Automation
4. Why This One
5. Step-by-Step Build Plan
6. Suggested Tools / Stack

## Setup

Requires Python 3.10+ (developed on 3.14.5).

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder with your Groq API key:

```
GROQ_API_KEY=your_key_here
```

Get a key at https://console.groq.com/keys.

## Usage

**Pass the workflow as an argument:**

```bash
python main.py "Every morning I pull 3 CSV reports, clean them in Excel, and email a summary."
```

**Pipe it from a file:**

```bash
cat workflow.txt | python main.py
```

**Interactive prompt** (press Enter to use the built-in sample):

```bash
python main.py
```

**Use it in code:**

```python
from main import diagnose

plan = diagnose("I manually reconcile invoices against the ledger every week...")
print(plan)
```

## Evaluating a plan (LLM-as-judge)

`evaluate(workflow_description, plan)` scores a diagnosis plan against its source
workflow on 15 criteria (see `eval_prompt.md`) and returns a dict:

```python
from main import diagnose, evaluate

plan = diagnose(workflow)
result = evaluate(workflow, plan)
result["overall_score"]       # e.g. 85.05
result["breakdown"]           # 15 rows: {principle, score, comment}
result["top_3_improvements"]  # list
result["rewrite"]             # full 100/100 rewrite
```

Or from the CLI, add `--eval`:

```bash
python main.py --eval "Every week I export new signups from our CRM..."
```

The judge uses a **stronger model** (`llama-3.3-70b-versatile`) than the generator,
since self-grading with the small model is lenient. Override it:

```bash
EVAL_MODEL=llama-3.1-8b-instant python main.py --eval "..."
```

## Run the API

A FastAPI service exposes the tool over HTTP.

```bash
uvicorn api:app --reload
```

Open http://127.0.0.1:8000/docs for interactive Swagger docs. Endpoints:

- `GET  /health` — liveness check.
- `POST /diagnose` — body `{"workflow_description": "..."}` → `{"plan": "..."}`.
- `POST /evaluate` — body `{"workflow_description": "...", "plan": "..."}` → score dict.

Example:

```bash
curl -X POST http://127.0.0.1:8000/diagnose \
  -H "Content-Type: application/json" \
  -d '{"workflow_description": "Every Monday I copy ticket counts into a spreadsheet and build a chart."}'
```

## Tests

```bash
pytest               # 8 unit tests — fast, offline, LLM mocked (no API key needed)
pytest -m integration   # 1 live end-to-end test — hits real Groq (needs GROQ_API_KEY + network)
```

Integration tests are excluded from the default run (see `pytest.ini`) and skip
gracefully if `GROQ_API_KEY` is not set.

## Notes

- `llama-3.1-8b-instant` is fast and cheap. For sharper diagnoses, swap the
  `MODEL` constant in `main.py` to `llama-3.3-70b-versatile`.
- Adjust `temperature` in `main.py` for more (higher) or less (lower) varied output.
- `MODEL` = generator, `EVAL_MODEL` = judge. Keeping them different avoids a model
  grading its own work.
