from datetime import date

import pytest
from pydantic import ValidationError

from models import GoalLevel, LearningGoal


def test_goal_defaults():
    goal = LearningGoal(subject="Physics", target="score 80%")

    assert goal.level is GoalLevel.INTERMEDIATE
    assert goal.language == "en"
    assert goal.deadline is None


def test_goal_strips_whitespace():
    goal = LearningGoal(subject="  Physics  ", target="  score 80%  ")

    assert goal.subject == "Physics"
    assert goal.target == "score 80%"


def test_goal_accepts_iso_deadline():
    goal = LearningGoal(subject="Physics", target="pass", deadline="2026-11-01")

    assert goal.deadline == date(2026, 11, 1)


@pytest.mark.parametrize("field", ["subject", "target"])
def test_goal_rejects_empty(field):
    payload = {"subject": "Physics", "target": "pass"}
    payload[field] = "   "

    with pytest.raises(ValidationError):
        LearningGoal(**payload)
