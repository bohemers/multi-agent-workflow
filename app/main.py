from __future__ import annotations

from fastapi import FastAPI

from app.core.workflow import MultiAgentWorkflow
from app.models.schemas import TaskRequest, WorkflowReport

app = FastAPI(
    title="Multi-Agent Workflow",
    version="0.1.0",
    description="Planner, Search, Analysis, and Report agents with mock tool calling and structured reports.",
)

workflow = MultiAgentWorkflow()


@app.get("/")
async def root() -> dict:
    return {
        "name": "Multi-Agent Workflow",
        "docs": "/docs",
        "run_endpoint": "/workflow/run",
    }


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.post("/workflow/run", response_model=WorkflowReport)
async def run_workflow(request: TaskRequest) -> WorkflowReport:
    return workflow.run(request)
