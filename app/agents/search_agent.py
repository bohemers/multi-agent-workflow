from __future__ import annotations

from app.agents.base import BaseAgent
from app.models.schemas import EvidenceBundle, ToolCall, WorkflowPlan
from app.tools.mock_search import MockSearchTool


class SearchAgent(BaseAgent):
    """Runs planned queries through a search tool and records traceable evidence."""

    name = "search_agent"

    def __init__(self, search_tool: MockSearchTool | None = None) -> None:
        self.search_tool = search_tool or MockSearchTool()

    def run(
        self,
        plan: WorkflowPlan,
        max_results: int,
    ) -> tuple[list[EvidenceBundle], list[ToolCall]]:
        evidence: list[EvidenceBundle] = []
        tool_calls: list[ToolCall] = []

        for step in plan.steps:
            for query in step.queries:
                with self.timed() as elapsed_ms:
                    results = self.search_tool.search(query=query, top_k=max_results)
                evidence.append(
                    EvidenceBundle(
                        step_id=step.step_id,
                        query=query,
                        results=results,
                    )
                )
                top_ids = [item.source_id for item in results[:3]]
                tool_calls.append(
                    ToolCall(
                        agent=self.name,
                        tool_name="mock_search",
                        input={"query": query, "top_k": max_results},
                        output_summary=f"returned {len(results)} results; top sources: {top_ids}",
                        latency_ms=elapsed_ms(),
                    )
                )

        return evidence, tool_calls
