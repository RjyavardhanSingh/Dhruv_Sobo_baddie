from pathlib import Path

import pytest

from context import ContextBuilder, ContextBuildError, build_context
from models import LearningGoal, MaterialKind

PDF_PATH = Path(__file__).parent.parent / "data" / "test_biology.pdf"


def _goal() -> LearningGoal:
    return LearningGoal(subject="Biology", target="score 80%")


def test_build_context_from_pdf():
    context = ContextBuilder().with_goal(_goal()).add_file(PDF_PATH).build()

    assert context.goal.subject == "Biology"
    assert context.stats.source_count == 1
    assert context.stats.page_count == 3
    assert context.stats.word_count > 0
    assert context.stats.reading_minutes >= 1
    assert context.sources[0].kind is MaterialKind.PDF


def test_build_context_combines_material_types():
    context = (
        ContextBuilder()
        .with_goal(_goal())
        .add_file(PDF_PATH)
        .add_text("Extra notes about cells.", name="notes.txt")
        .add_text(
            "# Photosynthesis\n\nLight to energy.",
            name="extra.md",
            kind=MaterialKind.MARKDOWN,
        )
        .build()
    )

    assert context.stats.source_count == 3
    assert context.stats.page_count == 3 + 1 + 1
    assert len(context.sources) == 3


def test_build_context_requires_goal():
    with pytest.raises(ContextBuildError, match="goal is required"):
        ContextBuilder().add_text("some notes").build()


def test_build_context_requires_readable_source():
    with pytest.raises(ContextBuildError, match="at least one source"):
        ContextBuilder().with_goal(_goal()).build()


def test_build_context_ignores_empty_sources():
    with pytest.raises(ContextBuildError, match="at least one source"):
        ContextBuilder().with_goal(_goal()).add_text("   ").build()


def test_context_id_is_stable():
    first = ContextBuilder().with_goal(_goal()).add_file(PDF_PATH).build()
    second = ContextBuilder().with_goal(_goal()).add_file(PDF_PATH).build()

    assert first.context_id == second.context_id


def test_context_id_changes_with_goal():
    other = LearningGoal(subject="Biology", target="score 95%")
    first = ContextBuilder().with_goal(_goal()).add_file(PDF_PATH).build()
    second = ContextBuilder().with_goal(other).add_file(PDF_PATH).build()

    assert first.context_id != second.context_id


def test_build_context_convenience_wrapper():
    context = build_context(goal=_goal(), files=[PDF_PATH], text="Pasted notes.")

    assert context.stats.source_count == 2
