from app.core.workflow import MultiAgentWorkflow
from app.models.schemas import TaskRequest
from app.tools.mock_search import MockSearchTool


def test_workflow_generates_structured_report() -> None:
    request = TaskRequest(
        task="分析一个 AI Agent 项目如何体现工程深度",
        audience="AI internship interviewer",
        depth="deep",
    )

    report = MultiAgentWorkflow().run(request)

    assert report.intent == "agent_workflow"
    assert len(report.plan.steps) >= 4
    assert report.findings
    assert report.tool_calls
    assert "## Key Findings" in report.markdown
    assert "Confidence" in report.markdown


def test_mock_search_returns_ranked_agent_sources() -> None:
    results = MockSearchTool().search("agent workflow tool calling state management")

    assert results
    assert results[0].score >= results[-1].score
    assert any("agent" in " ".join(result.tags) for result in results)
