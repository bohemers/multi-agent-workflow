from __future__ import annotations

from app.agents.base import BaseAgent
from app.models.schemas import (
    AnalysisResult,
    TaskRequest,
    ToolCall,
    WorkflowPlan,
    WorkflowReport,
)


class ReportAgent(BaseAgent):
    """Formats the workflow state into Markdown and structured JSON."""

    name = "report_agent"

    def run(
        self,
        request: TaskRequest,
        plan: WorkflowPlan,
        analysis: AnalysisResult,
        tool_calls: list[ToolCall],
    ) -> WorkflowReport:
        markdown = self._to_markdown(request, plan, analysis, tool_calls)
        return WorkflowReport(
            task=request.task,
            intent=plan.intent,
            plan=plan,
            findings=analysis.findings,
            recommendations=analysis.recommendations,
            limitations=analysis.limitations,
            tool_calls=tool_calls,
            markdown=markdown,
        )

    def _to_markdown(
        self,
        request: TaskRequest,
        plan: WorkflowPlan,
        analysis: AnalysisResult,
        tool_calls: list[ToolCall],
    ) -> str:
        lines: list[str] = [
            "# Multi-Agent Analysis Report",
            "",
            "## Executive Summary",
            f"- Task: {request.task}",
            f"- Intent: `{plan.intent}`",
            f"- Depth: `{request.depth}`",
            f"- Planned steps: {len(plan.steps)}",
            f"- Tool calls: {len(tool_calls)}",
            "",
            "## Workflow Plan",
        ]

        for step in plan.steps:
            lines.extend(
                [
                    f"### {step.step_id}. {step.objective}",
                    f"- Agent hint: `{step.agent_hint}`",
                    f"- Expected output: {step.expected_output}",
                    f"- Queries: {', '.join(step.queries)}",
                    "",
                ]
            )

        lines.append("## Key Findings")
        for index, finding in enumerate(analysis.findings, start=1):
            lines.extend(
                [
                    f"### {index}. {finding.title}",
                    f"- Step: `{finding.step_id}`",
                    f"- Confidence: `{finding.confidence}`",
                    f"- Evidence: {', '.join(finding.evidence_ids) or 'N/A'}",
                    f"- Summary: {finding.summary}",
                    "- Implications:",
                ]
            )
            lines.extend(f"  - {item}" for item in finding.implications)
            lines.append("- Risks:")
            lines.extend(f"  - {item}" for item in finding.risks)
            lines.append("")

        lines.append("## Recommendations")
        lines.extend(f"- {item}" for item in analysis.recommendations)
        lines.extend(["", "## Limitations"])
        lines.extend(f"- {item}" for item in analysis.limitations)

        lines.extend(["", "## Tool Trace"])
        for call in tool_calls:
            lines.append(
                f"- `{call.agent}` called `{call.tool_name}` in {call.latency_ms}ms: {call.output_summary}"
            )

        return "\n".join(lines).strip() + "\n"
