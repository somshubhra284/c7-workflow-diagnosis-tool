"""Tests for the FastAPI endpoints in api.py.

These are unit tests for the API layer: the LLM calls (diagnose / evaluate) are
mocked at the `api` module boundary, so no network calls are made and no Groq API
key is required. They verify routing, request validation, response shape, and
error handling — not the quality of the LLM output.

Run with:
    pytest -v
"""

import os

import pytest
from fastapi.testclient import TestClient

import api

client = TestClient(api.app)


# --- /health ---------------------------------------------------------------


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Workflow Diagnosis Tool API",
    }


# --- /diagnose -------------------------------------------------------------


def test_diagnose_happy_path(monkeypatch):
    captured = {}

    def fake_diagnose(workflow_description):
        captured["input"] = workflow_description
        return "## Workflow Summary\nMocked plan."

    monkeypatch.setattr(api, "diagnose", fake_diagnose)

    workflow = "Every Monday I copy ticket counts into a spreadsheet and build a chart."
    response = client.post("/diagnose", json={"workflow_description": workflow})

    assert response.status_code == 200
    assert response.json() == {"plan": "## Workflow Summary\nMocked plan."}
    # The endpoint passed the request body straight through to diagnose().
    assert captured["input"] == workflow


def test_diagnose_rejects_too_short_input():
    response = client.post("/diagnose", json={"workflow_description": "hi"})
    assert response.status_code == 422


def test_diagnose_rejects_missing_field():
    response = client.post("/diagnose", json={})
    assert response.status_code == 422


def test_diagnose_llm_failure_returns_502(monkeypatch):
    def boom(workflow_description):
        raise RuntimeError("groq exploded")

    monkeypatch.setattr(api, "diagnose", boom)

    response = client.post(
        "/diagnose",
        json={"workflow_description": "A long enough workflow description here."},
    )
    assert response.status_code == 502
    assert "groq exploded" in response.json()["detail"]


# --- /evaluate -------------------------------------------------------------


def test_evaluate_happy_path(monkeypatch):
    fake_result = {
        "overall_score": 85.0,
        "breakdown": [{"principle": "Workflow Fidelity", "score": 6.7, "comment": "ok"}],
        "top_3_improvements": ["a", "b", "c"],
        "suggested_edits": ["edit one"],
        "rewrite": "rewritten plan",
    }

    def fake_evaluate(workflow_description, plan):
        return fake_result

    monkeypatch.setattr(api, "evaluate", fake_evaluate)

    response = client.post(
        "/evaluate",
        json={
            "workflow_description": "A long enough workflow description here.",
            "plan": "A long enough diagnosis plan here.",
        },
    )
    assert response.status_code == 200
    assert response.json() == fake_result


def test_evaluate_rejects_missing_plan():
    response = client.post(
        "/evaluate",
        json={"workflow_description": "A long enough workflow description here."},
    )
    assert response.status_code == 422


def test_evaluate_llm_failure_returns_502(monkeypatch):
    def boom(workflow_description, plan):
        raise RuntimeError("judge exploded")

    monkeypatch.setattr(api, "evaluate", boom)

    response = client.post(
        "/evaluate",
        json={
            "workflow_description": "A long enough workflow description here.",
            "plan": "A long enough diagnosis plan here.",
        },
    )
    assert response.status_code == 502
    assert "judge exploded" in response.json()["detail"]


# --- integration (real Groq call) ------------------------------------------
# Skipped by default (see pytest.ini). Run explicitly with: pytest -m integration


@pytest.mark.integration
def test_diagnose_end_to_end_real_groq():
    """Full stack: HTTP -> api -> main.diagnose -> real Groq. No mocking."""
    if not os.environ.get("GROQ_API_KEY"):
        pytest.skip("GROQ_API_KEY not set; skipping live integration test.")

    workflow = (
        "Every morning I download 3 CSV sales reports from our dashboard, clean "
        "the columns in Excel, combine them, calculate regional totals, and email "
        "a summary to my manager. It takes about an hour."
    )
    response = client.post("/diagnose", json={"workflow_description": workflow})

    assert response.status_code == 200
    plan = response.json()["plan"]
    assert isinstance(plan, str) and plan.strip()
    # The real LLM should produce the structured sections the prompt asks for.
    assert "## Workflow Summary" in plan
    assert "## Best First Automation" in plan
