"""FastAPI service exposing the workflow diagnosis tool.

Run with:
    uvicorn api:app --reload

Then open http://127.0.0.1:8000/docs for interactive docs.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from main import diagnose, evaluate

app = FastAPI(
    title="Workflow Diagnosis Tool",
    description="Turn an analyst's workflow description into a first-automation plan.",
    version="1.0.0",
)


class DiagnoseRequest(BaseModel):
    workflow_description: str = Field(
        ...,
        min_length=10,
        description="Plain-English description of the analyst's workflow.",
        examples=[
            "Every morning I download 3 CSV sales reports, clean them in Excel, "
            "combine them, calculate regional totals, and email a summary to my manager."
        ],
    )


class DiagnoseResponse(BaseModel):
    plan: str


class EvaluateRequest(BaseModel):
    workflow_description: str = Field(
        ..., min_length=10, description="The input originally passed to diagnose()."
    )
    plan: str = Field(
        ..., min_length=10, description="The diagnosis plan returned by diagnose()."
    )


@app.get("/health")
def health() -> dict:
    """Liveness check."""
    return {"status": "ok"}


@app.get("/")
def root():
    return {"status": "ok", "message": "Workflow Diagnosis Tool API"}


@app.post("/diagnose", response_model=DiagnoseResponse)
def diagnose_endpoint(request: DiagnoseRequest) -> DiagnoseResponse:
    """Generate a first-automation diagnosis plan from a workflow description."""
    try:
        plan = diagnose(request.workflow_description)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {exc}")
    return DiagnoseResponse(plan=plan)


@app.post("/evaluate")
def evaluate_endpoint(request: EvaluateRequest) -> dict:
    """Score a diagnosis plan against its source workflow (LLM-as-judge)."""
    try:
        return evaluate(request.workflow_description, request.plan)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {exc}")
