from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Callable, Iterator


class BaseAgent:
    """Shared helpers for deterministic agents in this demo workflow."""

    name: str = "base_agent"

    @contextmanager
    def timed(self) -> Iterator[Callable[[], int]]:
        start = time.perf_counter()

        def elapsed_ms() -> int:
            return round((time.perf_counter() - start) * 1000)

        yield elapsed_ms
