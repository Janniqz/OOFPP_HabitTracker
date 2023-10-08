from datetime import datetime
from unittest.mock import MagicMock

import pytest

from classes.orm.habit import Habit
from classes.periodicity import Periodicity


@pytest.fixture
def habit() -> Habit:
    """
    Returns a Habit object for testing.
    """
    return Habit(habit_id=1, name="Test Habit", periodicity=Periodicity.Daily, creation_date=datetime.now())

# region Update


def test_update_name(habit: Habit) -> None:
    """
    Tests that the Habit's name is updated correctly.
    """
    session = MagicMock()
    new_name = "Updated Test Habit"

    changes_made = habit.update(session=session, new_name=new_name)

    session.commit.assert_called_once()
    assert changes_made is True
    assert habit.name == new_name


def test_update_periodicity(habit: Habit) -> None:
    """
    Tests that the Habit's periodicity is updated correctly.
    """
    session = MagicMock()
    new_periodicity = Periodicity.Weekly

    changes_made = habit.update(session=session, new_periodicity=new_periodicity)

    session.commit.assert_called_once()
    assert changes_made is True
    assert habit.periodicity == new_periodicity


def test_update_same_data(habit: Habit) -> None:
    """
    Tests that the Habit's name and Periodicity are not updated if their existing values are provided.
    """
    session = MagicMock()

    # Attempt to update with same data
    habit_name = habit.name
    habit_periodicity = habit.periodicity
    changes_made = habit.update(session=session, new_name=habit_name, new_periodicity=habit_periodicity)

    # Commit should not be called as no changes were made
    session.commit.assert_not_called()
    assert changes_made is False


def test_update_no_data(habit: Habit) -> None:
    """
    Tests that the Habit's name and Periodicity are not updated if no data is provided.
    """
    session = MagicMock()

    # Attempt to update without providing new name or periodicity
    changes_made = habit.update(session=session)

    # Commit should not be called as no changes were made
    session.commit.assert_not_called()
    assert changes_made is False


# endregion
