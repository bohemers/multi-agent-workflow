from __future__ import annotations

from collections import defaultdict

from app.agents.base import BaseAgent
from app.models.schemas import (
    AnalysisResult,
    AnalyticalFinding,
    EvidenceBundle,
    SearchResult,
    WorkflowPlan,
)


class AnalysisAgent(BaseAgent):
    """Converts retrieved evidence into findings with confidence scores."""

    name = "analysis_agent"

    def run(
        self,
        plan: WorkflowPlan,
        evidence: list[EvidenceBundle],
    ) -> AnalysisResult:
        evidence_by_step: dict[str, list[SearchResult]] = defaultdict(list)
        for bundle in evidence:
            evidence_by_step[bundle.step_id].extend(bundle.results)

        findings: list[AnalyticalFinding] = []
        limitations: list[str] = []

        for step in plan.steps:
            results = self._deduplicate(evidence_by_step.get(step.step_id, []))
            confidence = self._confidence(results)
            if confidence < 0.45:
                limitations.append(
                    f"{step.step_id} 的证据覆盖不足，相关结论应作为假设而不是强判断。"
                )

            findings.append(
                AnalyticalFinding(
                    step_id=step.step_id,
                    title=self._finding_title(step.objective),
                    summary=self._build_summary(step.objective, results, confidence),
                    evidence_ids=[item.source_id for item in results[:4]],
                    confidence=confidence,
                    implications=self._build_implications(step.objective, plan.intent),
                    risks=self._build_risks(step.objective, confidence),
                )
            )

        recommendations = self._build_recommendations(plan.intent, findings)
        if not limitations:
            limitations.append("当前报告基于本地 mock corpus，不能替代真实业务数据和线上实验。")

        return AnalysisResult(
            findings=findings,
            recommendations=recommendations,
            limitations=limitations,
        )

    def _deduplicate(self, results: list[SearchResult]) -> list[SearchResult]:
        seen: set[str] = set()
        unique: list[SearchResult] = []
        for item in sorted(results, key=lambda result: result.score, reverse=True):
            if item.source_id in seen:
                continue
            seen.add(item.source_id)
            unique.append(item)
        return unique

    def _confidence(self, results: list[SearchResult]) -> float:
        if not results:
            return 0.2
        top_scores = [item.score for item in results[:4]]
        score_signal = min(1.0, sum(top_scores) / max(1, len(top_scores)))
        coverage_signal = min(1.0, len(results) / 4)
        confidence = 0.7 * score_signal + 0.3 * coverage_signal
        return round(max(0.2, min(confidence, 0.95)), 2)

    def _finding_title(self, objective: str) -> str:
        if "orchestration" in objective.lower() or "workflow" in objective.lower():
            return "Agent workflow needs explicit orchestration and tool contracts"
        if "retrieval" in objective.lower() or "embedding" in objective.lower():
            return "RAG quality depends on retrieval design and answer grounding"
        if "trade" in objective.lower() or "failure" in objective.lower():
            return "Technical depth comes from trade-offs, failure modes, and observability"
        if "action" in objective.lower() or "report" in objective.lower():
            return "Reports should convert analysis into concrete next actions"
        if "goal" in objective.lower():
            return "The task needs clear goals and measurable success criteria"
        return "Implementation patterns should be connected to evaluation outcomes"

    def _build_summary(
        self,
        objective: str,
        results: list[SearchResult],
        confidence: float,
    ) -> str:
        if not results:
            return (
                f"针对 `{objective}` 暂未检索到强相关证据。建议把该部分作为待验证假设，"
                "并在真实项目中补充数据源或实验结果。"
            )

        lead = results[0]
        support = ", ".join(item.source_id for item in results[:3])
        return (
            f"围绕 `{objective}`，最相关证据来自 {lead.source_id}：{lead.title}。"
            f"综合 {support} 的内容，当前判断置信度为 {confidence}，"
            "适合用于形成设计建议，但仍应保留验证步骤。"
        )

    def _build_implications(self, objective: str, intent: str) -> list[str]:
        implications = [
            "把输入、输出、工具调用和状态变化显式建模，有利于面试官理解系统边界。",
            "报告中的结论应引用证据或说明假设，避免看起来像一次性文本生成。",
        ]
        if intent == "agent_workflow":
            implications.append("Agent 拆分要服务于任务流转，不能只是按名字拆类。")
        if intent == "rag_system_design":
            implications.append("RAG 项目需要展示 chunk、embedding、retrieval、generation 的质量控制。")
        if "failure" in objective.lower():
            implications.append("失败处理、重试和低置信度提示会显著提升项目可信度。")
        return implications

    def _build_risks(self, objective: str, confidence: float) -> list[str]:
        risks = []
        if confidence < 0.55:
            risks.append("证据不足时，报告可能给出过度确定的结论。")
        if "tool" in objective.lower() or "workflow" in objective.lower():
            risks.append("如果工具接口没有 schema 和日志，后续接入真实工具会难以调试。")
        if "report" in objective.lower():
            risks.append("如果报告只有自然语言，没有结构化字段，前端和 API 复用成本会变高。")
        return risks or ["当前风险主要来自 mock 数据与真实生产环境之间的差距。"]

    def _build_recommendations(
        self,
        intent: str,
        findings: list[AnalyticalFinding],
    ) -> list[str]:
        recommendations = [
            "保留 workflow trace，让每一次工具调用、证据来源和分析结论都能被追踪。",
            "把 Agent 输入输出定义成 Pydantic schema，降低后续接真实 LLM 时的不确定性。",
            "为低置信度结论增加 limitations，不把 mock 结果包装成真实数据。",
        ]
        if intent == "agent_workflow":
            recommendations.insert(
                0,
                "优先展示 Planner -> Search -> Analysis -> Report 的状态流转，而不是只展示单轮问答。",
            )
        if intent == "rag_system_design":
            recommendations.insert(
                0,
                "补充检索评估指标，例如 top-k 命中、引用覆盖率和答案 groundedness。",
            )

        low_confidence = [finding for finding in findings if finding.confidence < 0.55]
        if low_confidence:
            recommendations.append("对低置信度步骤补充更多数据源或人工校验入口。")
        return recommendations
