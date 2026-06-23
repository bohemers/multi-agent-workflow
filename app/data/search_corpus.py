from __future__ import annotations

SEARCH_CORPUS = [
    {
        "source_id": "SRC-001",
        "title": "Agent workflow architecture with explicit state transitions",
        "url": "mock://agent-workflow/state-transitions",
        "source": "local-architecture-note",
        "published_at": "2026-01-12",
        "tags": ["agent", "workflow", "orchestrator", "state management"],
        "content": (
            "A credible multi-agent system should model state transitions explicitly. "
            "Planner, tool executor, analyzer, and reporter should exchange structured objects "
            "instead of hidden strings. This makes traces, retries, and evaluation easier."
        ),
    },
    {
        "source_id": "SRC-002",
        "title": "Tool calling contracts for reliable AI applications",
        "url": "mock://agent-workflow/tool-contracts",
        "source": "local-engineering-note",
        "published_at": "2026-02-03",
        "tags": ["tool calling", "schema", "observability", "testing"],
        "content": (
            "Tool calls should have stable schemas, typed inputs, typed outputs, "
            "latency records, error handling, and output summaries. Without contracts, "
            "a demo becomes difficult to debug when connected to real APIs."
        ),
    },
    {
        "source_id": "SRC-003",
        "title": "Planner agents should decompose tasks into measurable steps",
        "url": "mock://agent-workflow/planner",
        "source": "local-agent-note",
        "published_at": "2025-12-19",
        "tags": ["planner", "task decomposition", "success criteria"],
        "content": (
            "Planner agents are useful when they create subgoals, success criteria, "
            "constraints, and tool strategies. A planner that only rewrites the prompt "
            "does not add much engineering value."
        ),
    },
    {
        "source_id": "SRC-004",
        "title": "Evidence-grounded analysis improves report credibility",
        "url": "mock://analysis/evidence-grounding",
        "source": "local-analysis-note",
        "published_at": "2026-02-21",
        "tags": ["analysis", "evidence", "confidence", "report"],
        "content": (
            "Analysis agents should connect findings with evidence identifiers, "
            "confidence scores, risks, and limitations. This prevents reports from looking "
            "like ungrounded long-form generation."
        ),
    },
    {
        "source_id": "SRC-005",
        "title": "RAG system design checklist",
        "url": "mock://rag/system-design-checklist",
        "source": "local-rag-note",
        "published_at": "2026-03-07",
        "tags": ["rag", "chunking", "embedding", "semantic search", "qa"],
        "content": (
            "A RAG system typically includes document ingestion, chunking, embedding, "
            "vector retrieval, reranking, prompt assembly, grounded answer generation, "
            "and citation-aware evaluation."
        ),
    },
    {
        "source_id": "SRC-006",
        "title": "Retrieval quality matters more than prompt polish in RAG",
        "url": "mock://rag/retrieval-quality",
        "source": "local-rag-eval-note",
        "published_at": "2026-03-15",
        "tags": ["rag", "retrieval", "embedding", "evaluation"],
        "content": (
            "Top-k recall, chunk granularity, metadata filters, and reranking quality "
            "strongly affect RAG answer quality. Poor retrieval cannot be fully fixed "
            "by prompt engineering."
        ),
    },
    {
        "source_id": "SRC-007",
        "title": "FastAPI project boundaries for AI services",
        "url": "mock://backend/fastapi-ai-service",
        "source": "local-backend-note",
        "published_at": "2026-01-29",
        "tags": ["fastapi", "service layer", "schema", "testing"],
        "content": (
            "A maintainable AI backend separates API routes, schemas, services, agents, "
            "and data adapters. Pydantic models make request and response contracts visible."
        ),
    },
    {
        "source_id": "SRC-008",
        "title": "Portfolio projects should be runnable and inspectable",
        "url": "mock://portfolio/runnable-projects",
        "source": "local-portfolio-note",
        "published_at": "2026-04-01",
        "tags": ["portfolio", "github", "readme", "demo", "technical credibility"],
        "content": (
            "A strong internship portfolio should include clear README files, local run commands, "
            "tests, realistic mock data, screenshots or output samples, and honest limitations."
        ),
    },
    {
        "source_id": "SRC-009",
        "title": "Failure handling in agentic systems",
        "url": "mock://agent-workflow/failure-handling",
        "source": "local-reliability-note",
        "published_at": "2026-02-18",
        "tags": ["failure mode", "risk", "retry", "observability"],
        "content": (
            "Agent systems should expose low-confidence outputs, empty search results, "
            "tool errors, timeout behavior, and retry or fallback policies. These details "
            "often separate real engineering work from shallow demos."
        ),
    },
    {
        "source_id": "SRC-010",
        "title": "Report generation should serve both humans and machines",
        "url": "mock://report/structured-output",
        "source": "local-report-note",
        "published_at": "2026-03-24",
        "tags": ["report", "recommendation", "structured output", "json"],
        "content": (
            "Reports are easier to reuse when the system returns both Markdown and structured JSON. "
            "The Markdown helps human reading, while JSON fields help API clients, dashboards, "
            "and automated evaluation."
        ),
    },
]
