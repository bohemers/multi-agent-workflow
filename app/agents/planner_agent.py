from __future__ import annotations

from app.agents.base import BaseAgent
from app.models.schemas import PlanStep, TaskRequest, WorkflowPlan
from app.utils.text import normalize_spaces


class PlannerAgent(BaseAgent):
    """Turns an open-ended user task into explicit research steps."""

    name = "planner_agent"

    def run(self, request: TaskRequest) -> WorkflowPlan:
        task = normalize_spaces(request.task)
        intent = self._classify_intent(task)
        focus_areas = self._select_focus_areas(intent, request.depth)

        steps = [
            PlanStep(
                step_id=f"S{i + 1}",
                objective=area["objective"],
                agent_hint=area["agent_hint"],
                queries=self._build_queries(area["keywords"]),
                expected_output=area["expected_output"],
            )
            for i, area in enumerate(focus_areas)
        ]

        assumptions = [
            "默认不使用真实联网搜索，检索结果来自本地 mock corpus。",
            "默认报告面向技术面试官和项目评审者，强调工程结构与可解释性。",
        ]
        if request.audience:
            assumptions.append(f"报告读者定位为：{request.audience}。")

        return WorkflowPlan(
            original_task=task,
            intent=intent,
            assumptions=assumptions,
            steps=steps,
            success_criteria=[
                "任务被拆解为可执行步骤，而不是一次性生成答案。",
                "每个结论尽量能追溯到检索证据或明确假设。",
                "最终报告包含建议、风险、限制和下一步行动。",
            ],
        )

    def _classify_intent(self, task: str) -> str:
        lower = task.lower()
        if any(word in lower for word in ["rag", "知识库", "向量", "检索增强"]):
            return "rag_system_design"
        if any(word in lower for word in ["agent", "智能体", "workflow", "工具调用"]):
            return "agent_workflow"
        if any(word in lower for word in ["fastapi", "api", "后端", "服务"]):
            return "backend_architecture"
        if any(word in lower for word in ["简历", "作品集", "github", "面试"]):
            return "portfolio_positioning"
        return "technical_analysis"

    def _select_focus_areas(self, intent: str, depth: str) -> list[dict]:
        common = [
            {
                "objective": "Clarify task goal and evaluation criteria",
                "agent_hint": "planner",
                "keywords": ["goal", "evaluation", "success criteria"],
                "expected_output": "明确任务目标、验收标准和隐含约束。",
            },
            {
                "objective": "Collect relevant implementation patterns",
                "agent_hint": "search",
                "keywords": ["architecture", "tool calling", "state management"],
                "expected_output": "找到可支撑设计判断的实现模式和证据。",
            },
            {
                "objective": "Analyze trade-offs and failure modes",
                "agent_hint": "analysis",
                "keywords": ["tradeoff", "failure mode", "risk", "observability"],
                "expected_output": "形成带风险、取舍和置信度的分析结论。",
            },
            {
                "objective": "Generate structured action plan",
                "agent_hint": "report",
                "keywords": ["report", "recommendation", "next steps"],
                "expected_output": "输出面向读者的结构化报告和行动建议。",
            },
        ]

        intent_specific = {
            "rag_system_design": {
                "objective": "Evaluate retrieval, chunking, embedding, and answer generation design",
                "agent_hint": "analysis",
                "keywords": ["rag", "chunking", "embedding", "semantic search", "qa"],
                "expected_output": "说明 RAG 系统的关键模块和质量控制点。",
            },
            "agent_workflow": {
                "objective": "Evaluate agent decomposition, tool contracts, and workflow orchestration",
                "agent_hint": "analysis",
                "keywords": ["agent workflow", "planner", "tool calling", "orchestrator"],
                "expected_output": "说明多智能体系统如何拆解任务、调用工具并保留执行轨迹。",
            },
            "backend_architecture": {
                "objective": "Evaluate API boundaries, schema design, and service maintainability",
                "agent_hint": "analysis",
                "keywords": ["fastapi", "schema", "service layer", "testing"],
                "expected_output": "说明后端项目如何体现工程化边界和可测试性。",
            },
            "portfolio_positioning": {
                "objective": "Evaluate project story, recruiter readability, and technical credibility",
                "agent_hint": "analysis",
                "keywords": ["portfolio", "readme", "technical credibility", "demo"],
                "expected_output": "说明作品集如何兼顾招聘展示和真实可运行性。",
            },
        }

        selected = common[:]
        if intent in intent_specific:
            selected.insert(2, intent_specific[intent])

        if depth == "quick":
            return selected[:3]
        if depth == "deep":
            return selected
        return selected[:4]

    def _build_queries(self, keywords: list[str]) -> list[str]:
        return [
            keyword
            for keyword in keywords[:3]
        ]
