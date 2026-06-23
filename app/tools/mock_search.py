from __future__ import annotations

import re

from app.data.search_corpus import SEARCH_CORPUS
from app.models.schemas import SearchResult
from app.utils.text import extract_keywords


class MockSearchTool:
    """A deterministic search tool with simple relevance scoring."""

    def search(self, query: str, top_k: int = 4) -> list[SearchResult]:
        query_terms = extract_keywords(query)
        scored: list[SearchResult] = []

        for item in SEARCH_CORPUS:
            score = self._score_item(query_terms, item)
            if score <= 0:
                continue
            scored.append(
                SearchResult(
                    source_id=item["source_id"],
                    title=item["title"],
                    url=item["url"],
                    source=item["source"],
                    published_at=item["published_at"],
                    tags=item["tags"],
                    content=item["content"],
                    score=round(score, 2),
                )
            )

        if not scored:
            scored = self._fallback_results()

        return sorted(scored, key=lambda result: result.score, reverse=True)[:top_k]

    def _score_item(self, query_terms: set[str], item: dict) -> float:
        title = item["title"].lower()
        content = item["content"].lower()
        tags = " ".join(item["tags"]).lower()

        score = 0.0
        for term in query_terms:
            normalized = term.lower()
            if normalized in tags:
                score += 0.4
            if normalized in title:
                score += 0.35
            if normalized in content:
                score += 0.25

            if len(normalized) > 3:
                pattern = re.escape(normalized)
                score += min(0.2, len(re.findall(pattern, content)) * 0.05)

        return min(score, 1.0)

    def _fallback_results(self) -> list[SearchResult]:
        fallback = SEARCH_CORPUS[:2]
        return [
            SearchResult(
                source_id=item["source_id"],
                title=item["title"],
                url=item["url"],
                source=item["source"],
                published_at=item["published_at"],
                tags=item["tags"],
                content=item["content"],
                score=0.25,
            )
            for item in fallback
        ]
