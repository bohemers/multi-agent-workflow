from __future__ import annotations

import re


DOMAIN_TERMS = {
    "agent",
    "workflow",
    "planner",
    "search",
    "analysis",
    "report",
    "tool",
    "calling",
    "orchestrator",
    "state",
    "schema",
    "fastapi",
    "rag",
    "embedding",
    "retrieval",
    "semantic",
    "chunking",
    "qa",
    "portfolio",
    "github",
    "readme",
    "testing",
    "evaluation",
    "confidence",
    "risk",
    "智能体",
    "任务拆解",
    "工具调用",
    "工作流",
    "检索",
    "向量",
    "知识库",
    "报告",
    "证据",
    "置信度",
    "后端",
    "作品集",
    "面试",
    "简历",
}

STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "into",
    "from",
    "this",
    "that",
    "how",
    "what",
    "一个",
    "如何",
    "项目",
    "分析",
    "设计",
    "重点",
}


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_keywords(text: str) -> set[str]:
    lower = text.lower()
    terms: set[str] = set()

    for term in DOMAIN_TERMS:
        if term.lower() in lower:
            terms.add(term.lower())

    for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", lower):
        if token not in STOP_WORDS:
            terms.add(token)

    return terms
