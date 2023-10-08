from datetime import datetime, timedelta

import pytest

from classes.orm.habit import Habit
from classes.periodicity import Periodicity


@pytest.fixture
def habit() -> Habit:
    """
    Returns a Habit object with the following attributes:
    - habit_id: 1
    - name: Test Habit
    - periodicity: Periodicity.Daily
    - creation_date: datetime.now()
    """
    return Habit(habit_id=1, name='Test Habit', periodicity=Periodicity.Daily, creation_date=datetime.now())


# Daily

def test_same_day(habit: Habit) -> None:
    """
    Tests that the streak is not broken nor increased if the habit was completed on the same day.
    """
    habit.periodicity = Periodicity.Daily
    last_completion = datetime.now()
    result = habit._Habit__check_streak_validity(last_completion=last_completion)
    assert result is None


def test_previous_day(habit: Habit) -> None:
    """
    Tests that the streak is increased if the habit was completed on the previous day.
    """
    habit.periodicity = Periodicity.Daily
    last_completion = datetime.now() - timedelta(days=1)
    result = habit._Habit__check_streak_validity(last_completion=last_completion)
    assert result is True


def test_two_days(habit: Habit) -> None:
    """
    Tests that the streak is broken if the habit was completed two+ days ago.
    """
    habit.periodicity = Periodicity.Daily
    last_completion = datetime.now() - timedelta(days=2)
    result = habit._Habit__check_streak_validity(last_completion=last_completion)
    assert result is False


# Weekly

def test_same_week(habit: Habit) -> None:
    """
    Tests that the streak is not broken nor increased if the habit was completed in the same week.
    """
    habit.periodicity = Periodicity.Weekly
    last_completion = datetime.now()
    result = habit._Habit__check_streak_validity(last_completion=last_completion)
    assert result is None


def test_previous_week(habit: Habit) -> None:
    """
    Tests that the streak is increased if the habit was completed in the previous week.
    """
    habit.periodicity = Periodicity.Weekly
    last_completion = datetime.now() - timedelta(days=7)
    result = habit._Habit__check_streak_validity(last_completion=last_completion)
    assert result is True


def test_two_weeks(habit: Habit) -> None:
    """
    Tests that the streak is broken if the habit was completed two+ weeks ago.
    """
    habit.periodicity = Periodicity.Weekly
    last_completion = datetime.now() - timedelta(days=14)
    result = habit._Habit__check_streak_validity(last_completion=last_completion)
    assert result is False
