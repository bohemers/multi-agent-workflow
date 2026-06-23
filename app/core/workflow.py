from __future__ import annotations

from app.agents.analysis_agent import AnalysisAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.report_agent import ReportAgent
from app.agents.search_agent import SearchAgent
from app.models.schemas import TaskRequest, WorkflowReport


class MultiAgentWorkflow:
    """Coordinates planner, search, analysis, and report agents."""

    def __init__(
        self,
        planner: PlannerAgent | None = None,
        searcher: SearchAgent | None = None,
        analyzer: AnalysisAgent | None = None,
        reporter: ReportAgent | None = None,
    ) -> None:
        self.planner = planner or PlannerAgent()
        self.searcher = searcher or SearchAgent()
        self.analyzer = analyzer or AnalysisAgent()
        self.reporter = reporter or ReportAgent()

    def run(self, request: TaskRequest) -> WorkflowReport:
        plan = self.planner.run(request)
        evidence, tool_calls = self.searcher.run(
            plan=plan,
            max_results=request.max_search_results,
        )
        analysis = self.analyzer.run(plan=plan, evidence=evidence)
        return self.reporter.run(
            request=request,
            plan=plan,
            analysis=analysis,
            tool_calls=tool_calls,
        )
