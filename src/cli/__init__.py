"""Command-line entry point for the self-learning platform."""

from __future__ import annotations

import argparse
import json
from datetime import date

from context import ContextBuilder, ContextBuildError
from models import GoalLevel, LearningGoal


def _parse_deadline(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent",
        description="Adaptive oral learning platform",
    )
    subparsers = parser.add_subparsers(dest="command")

    context = subparsers.add_parser(
        "build-context",
        help="Build a learning context from notes + goal",
    )
    context.add_argument("files", nargs="*", help="PDF, Markdown, or text files")
    context.add_argument("--text", help="Paste notes directly instead of using a file")
    context.add_argument("--text-name", default="pasted-notes.txt")
    context.add_argument("--subject", required=True, help="Subject being studied")
    context.add_argument("--target", required=True, help='Goal, e.g. "explain Gauss law"')
    context.add_argument(
        "--level",
        choices=[level.value for level in GoalLevel],
        default=GoalLevel.INTERMEDIATE.value,
    )
    context.add_argument("--deadline", help="ISO date, e.g. 2026-11-01")
    context.add_argument("--language", default="en", help="Answer language, e.g. en or hi")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "build-context":
        parser.print_help()
        return 0

    goal = LearningGoal(
        subject=args.subject,
        target=args.target,
        level=GoalLevel(args.level),
        deadline=_parse_deadline(args.deadline),
        language=args.language,
    )

    builder = ContextBuilder().with_goal(goal)
    for file in args.files:
        builder.add_file(file)
    if args.text:
        builder.add_text(args.text, name=args.text_name)

    try:
        context = builder.build()
    except ContextBuildError as error:
        parser.error(str(error))

    summary = {
        "context_id": context.context_id,
        "goal": context.goal.model_dump(mode="json"),
        "stats": context.stats.model_dump(),
        "sources": [
            {
                "name": source.name,
                "kind": source.kind.value,
                "pages": source.page_count,
                "words": source.word_count,
            }
            for source in context.sources
        ],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
