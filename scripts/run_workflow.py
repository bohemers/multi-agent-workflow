from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.workflow import MultiAgentWorkflow  # noqa: E402
from app.models.schemas import TaskRequest  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the multi-agent workflow demo.")
    parser.add_argument("--task", required=True, help="Task for the workflow to analyze.")
    parser.add_argument(
        "--audience",
        default="technical interviewer",
        help="Target audience for the generated report.",
    )
    parser.add_argument(
        "--depth",
        choices=["quick", "standard", "deep"],
        default="standard",
        help="Planning depth.",
    )
    parser.add_argument(
        "--max-search-results",
        type=int,
        default=4,
        help="Maximum search results per query.",
    )
    parser.add_argument("--json", action="store_true", help="Print structured JSON.")
    parser.add_argument("--output", help="Write Markdown report to this file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request = TaskRequest(
        task=args.task,
        audience=args.audience,
        depth=args.depth,
        max_search_results=args.max_search_results,
    )
    report = MultiAgentWorkflow().run(request)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report.markdown, encoding="utf-8")

    if args.json:
        print(json.dumps(report.model_dump(), ensure_ascii=False, indent=2))
    else:
        print(report.markdown)


if __name__ == "__main__":
    main()
