from unittest.mock import patch

import pytest
from click.testing import CliRunner
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from classes.orm.base import Base
from classes.orm.habit import Habit
from classes.periodicity import Periodicity
from modules.analytics import analytics

# Set up the SQLAlchemy session
engine = create_engine('sqlite:///:memory:')
session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Initialize your database tables
Base.metadata.create_all(bind=engine)


@pytest.fixture
def runner() -> CliRunner:
    """
    Returns a CLI Runner object.
    """
    return CliRunner()


@pytest.fixture(scope='module', autouse=True)
def create_test_habits() -> None:
    """
    Creates three test Habits for related tests.
    """
    session = session_maker()

    create_habit(session, habit_id=1, name='Test Habit 1', periodicity=Periodicity.Daily, streak=3, highest_streak=5)
    create_habit(session, habit_id=2, name='Test Habit 2', periodicity=Periodicity.Weekly, streak=4, highest_streak=8)
    create_habit(session, habit_id=3, name='Test Habit 3', periodicity=Periodicity.Daily, streak=5, highest_streak=7)


def create_habit(session: Session, habit_id: int, name: str, periodicity: Periodicity, streak: int, highest_streak: int) -> None:
    """
    Creates a Habit with the given parameters.

    :param session: The SQLAlchemy session object.
    :param habit_id: The ID of the Habit.
    :param name: The Name of the Habit.
    :param periodicity: The Periodicity of the Habit.
    :param streak: The current streak of the Habit.
    :param highest_streak: The highest streak of the Habit.
    """
    new_habit = Habit.create(session=session, habit_name=name, periodicity=periodicity)
    new_habit.habit_id = habit_id  # Overwrite with given id
    new_habit.streak = streak
    new_habit.highest_streak = highest_streak

    session.commit()

# region List


def test_list_default(runner: CliRunner) -> None:
    """
    Test the analytics list command without any flags.

    :param runner: The CLI Runner object.
    """
    with patch('modules.analytics.list_habits') as mock_list_habits:
        runner.invoke(cli=analytics, args=['list'], obj={'session_maker': session_maker})

    assert mock_list_habits.call_args.kwargs['habits'][0][0].habit_id == 1
    assert mock_list_habits.call_args.kwargs['habits'][1][0].habit_id == 2
    assert mock_list_habits.call_args.kwargs['habits'][2][0].habit_id == 3


def test_list_periodicity(runner: CliRunner) -> None:
    """
    Test the analytics list command with the -p flag.

    :param runner: The CLI Runner object.
    """
    with patch('modules.analytics.list_habits') as mock_list_habits:
        runner.invoke(cli=analytics, args=['list', '-p', 'daily'], obj={'session_maker': session_maker})

    assert len(mock_list_habits.call_args.kwargs['habits']) == 2


def test_list_sort_order(runner: CliRunner) -> None:
    """
    Test the analytics list command with the -s flag.

    :param runner: The CLI Runner object.
    """
    with patch('modules.analytics.list_habits') as mock_list_habits:
        runner.invoke(cli=analytics, args=['list', '-s', 'HighestStreak', '--desc'], obj={'session_maker': session_maker})

    assert mock_list_habits.call_args.kwargs['habits'][0][0].habit_id == 2
    assert mock_list_habits.call_args.kwargs['habits'][1][0].habit_id == 3
    assert mock_list_habits.call_args.kwargs['habits'][2][0].habit_id == 1


def test_list_periodicity_and_sort_order(runner: CliRunner) -> None:
    """
    Test the analytics list command with the -p and -s flags.

    :param runner: The CLI Runner object.
    """
    with patch('modules.analytics.list_habits') as mock_list_habits:
        runner.invoke(cli=analytics, args=['list', '-p', 'daily', '-s', 'HighestStreak', '--desc'], obj={'session_maker': session_maker})

    assert len(mock_list_habits.call_args.kwargs['habits']) == 2
    assert mock_list_habits.call_args.kwargs['habits'][0][0].habit_id == 3
    assert mock_list_habits.call_args.kwargs['habits'][1][0].habit_id == 1

# endregion

# region Streak


def test_longest_streak_habit_id(runner: CliRunner) -> None:
    """
    Test the analytics streak command with the -i flag.

    :param runner: The CLI Runner object.
    """
    result = runner.invoke(cli=analytics, args=['streak', '-i', '1'], obj={'session_maker': session_maker})
    assert f'The Habit Test Habit 1 has a longest streak of 5!' in result.output


def test_longest_streak_habit_name(runner: CliRunner) -> None:
    """
    Test the analytics streak command with the -n flag.

    :param runner: The CLI Runner object.
    """
    result = runner.invoke(cli=analytics, args=['streak', '-n', 'Test Habit 2'], obj={'session_maker': session_maker})
    assert f'The Habit Test Habit 2 has a longest streak of 8!' in result.output


def test_longest_streak(runner: CliRunner) -> None:
    """
    Test the analytics streak command without any flags.

    :param runner: The CLI Runner object.
    """
    result = runner.invoke(cli=analytics, args=['streak'], obj={'session_maker': session_maker})
    assert f'The Habit with the longest streak is: Test Habit 2 with a streak of 8!' in result.output


def test_longest_streak_active(runner: CliRunner) -> None:
    """
    Test the analytics streak command with the -a flag.

    :param runner: The CLI Runner object.
    """
    result = runner.invoke(cli=analytics, args=['streak', '-a'], obj={'session_maker': session_maker})
    assert f'The Habit with the longest active streak is: Test Habit 3 with a streak of 5!' in result.output


def test_longest_streak_active_specific(runner: CliRunner) -> None:
    """
    Test the analytics streak command with the -a flag and the -i flag.

    :param runner: The CLI Runner object.
    """
    result = runner.invoke(cli=analytics, args=['streak', '-i', '3', '-a'], obj={'session_maker': session_maker})
    assert f'The Habit Test Habit 3 has an active streak of 5!' in result.output


def test_longest_streak_no_habit(runner: CliRunner) -> None:
    """
    Test the analytics streak command with the -i flag and a non-existing Habit ID.

    :param runner: The CLI Runner object.
    """
    result = runner.invoke(cli=analytics, args=['streak', '-i', '9999'], obj={'session_maker': session_maker})
    assert 'No Matching Habit found.' in result.output


# endregion
