from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    task: str = Field(..., min_length=4, description="User task to analyze")
    audience: str = Field(
        default="technical interviewer",
        description="Who will read the final report",
    )
    depth: Literal["quick", "standard", "deep"] = "standard"
    max_search_results: int = Field(default=4, ge=1, le=8)


class PlanStep(BaseModel):
    step_id: str
    objective: str
    agent_hint: str
    queries: list[str]
    expected_output: str


class WorkflowPlan(BaseModel):
    original_task: str
    intent: str
    assumptions: list[str]
    steps: list[PlanStep]
    success_criteria: list[str]


class SearchResult(BaseModel):
    source_id: str
    title: str
    url: str
    source: str
    published_at: str
    tags: list[str]
    content: str
    score: float


class EvidenceBundle(BaseModel):
    step_id: str
    query: str
    results: list[SearchResult]


class ToolCall(BaseModel):
    agent: str
    tool_name: str
    input: dict[str, Any]
    output_summary: str
    latency_ms: int


class AnalyticalFinding(BaseModel):
    step_id: str
    title: str
    summary: str
    evidence_ids: list[str]
    confidence: float
    implications: list[str]
    risks: list[str]


class AnalysisResult(BaseModel):
    findings: list[AnalyticalFinding]
    recommendations: list[str]
    limitations: list[str]


class WorkflowReport(BaseModel):
    task: str
    intent: str
    plan: WorkflowPlan
    findings: list[AnalyticalFinding]
    recommendations: list[str]
    limitations: list[str]
    tool_calls: list[ToolCall]
    markdown: str
