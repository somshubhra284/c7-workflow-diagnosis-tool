# Task: Build `diagnose()` — Workflow Diagnosis Tool

## Goal
Turn an analyst student's plain-English workflow description into an actionable
**diagnosis plan** that identifies the single best first automation to build.

## LLM
Groq. `GROQ_API_KEY` lives in `.env`. SDK: `groq==1.5.0`.
Model: `llama-3.3-70b-versatile`.

## Task list
1. [x] `requirements.txt` — pin `groq==1.5.0`, `python-dotenv==1.2.2`.
       Python (3.14.5) recorded as a comment; pip cannot install Python itself.
2. [x] `main.py` — implement `diagnose(workflow_description)`:
       - load_dotenv -> GROQ_API_KEY
       - Groq client, system prompt ("automation diagnosis coach")
       - Output sections: Workflow Summary -> Automation Opportunities (ranked)
         -> Best First Automation -> Why this one -> Step-by-step build plan -> Tools/stack
       - return plan text; __main__ demo with sample analyst workflow
3. [x] Verify end-to-end against Groq. Confirmed: full 6-section plan returned.

## MVP scope
One function, one Groq call, strong prompt, returns text.
No streaming / retries / JSON schema.

## Changes log
- `requirements.txt`: created with groq==1.5.0, python-dotenv==1.2.2 + Python
  version note.
- `main.py`: implemented `diagnose(workflow_description) -> str`. Loads
  GROQ_API_KEY via load_dotenv, calls Groq chat.completions with model
  `llama-3.1-8b-instant` (model specified by the user in a code comment),
  temperature 0.4. System prompt = "automation diagnosis coach" enforcing 6
  fixed Markdown sections. `__main__` runs a sample analyst workflow demo.
- Verified: `python3 main.py` returns a complete diagnosis plan from Groq.

## Follow-up: CLI input + README
- `main.py`: added `_read_workflow_from_cli()` — reads workflow from (1) CLI
  args, (2) piped stdin, (3) interactive prompt, falling back to SAMPLE_WORKFLOW.
- `README.md`: created with setup, .env, and all three usage modes + model-swap note.
- Verified both CLI-arg and piped-stdin paths return tailored plans.

## Follow-up: eval prompt + evaluate() (LLM-as-judge)
- `eval_prompt.md`: standalone eval prompt (Ogilvy-style) scoring diagnose()
  output on 15 automation-quality criteria (~6.7 pts each).
- `main.py`: added `_client()` helper (shared Groq client), `EVAL_CRITERIA`,
  `EVAL_SYSTEM_PROMPT`, and `evaluate(workflow_description, plan) -> dict`.
  Uses temperature 0.0 + response_format json_object; returns
  overall_score / breakdown / top_3_improvements / suggested_edits / rewrite
  (falls back to {"raw": ...} on JSON parse failure).
- `__main__`: `--eval` flag runs diagnose() then evaluate() and prints score.
- Verified: `python3 main.py --eval "..."` returned 93.3/100 with full
  per-principle breakdown and top-3 improvements.

## Follow-up: separate judge model
- `main.py`: added `EVAL_MODEL` constant (default `llama-3.3-70b-versatile`,
  override via EVAL_MODEL env var). evaluate() now uses EVAL_MODEL instead of
  MODEL so the judge differs from the generator (avoids lenient self-grading).
- `README.md`: documented evaluate(), --eval, and EVAL_MODEL override.
- Verified: same plan scored 85.05/100 with the 70b judge (varied 5.0/6.0/6.7
  scores) vs 93.3 flat from the 8b self-grade — more discriminating.
