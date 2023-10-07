from typing import Optional, Tuple

import click
from click import Group, Context
from sqlalchemy import func
from sqlalchemy.orm import Session, Mapped

from classes.helpers.terminal_options import TerminalColor
from classes.orm.habit import Habit
from classes.orm.habit_entry import HabitEntry
from classes.periodicity import Periodicity
from helpers.cli_helper import colored_print, list_habits
from helpers.validations import validate_periodicity


@click.group()
def analytics() -> Group:
    """\b
    Module related to Habit Analytics
    """
    pass


@analytics.command(name='list')
@click.option('-p', '--period', 'periodicity', default=None, help='Periodicity of the Habit(s) that should be searched for.', type=click.UNPROCESSED, callback=validate_periodicity)
@click.option('-s', '--sort', 'sort_order', default='CreationDate', help='Field by which Habit(s) should be sorted by.', type=click.Choice(['ID', 'Name', 'Streak', 'HighestStreak', 'Periodicity', 'CreationDate', 'TotalCompletions', 'MostRecentCompletion'], case_sensitive=False))
@click.option('--asc', 'sort_order_asc', default=False, is_flag=True, help='Sort Habit(s) in ascending order.', type=bool)
@click.option('--desc', 'sort_order_desc', default=False, is_flag=True, help='Sort Habit(s) in descending order.', type=bool)
@click.pass_context
def analytics_list(ctx: Context, periodicity: Optional[Periodicity], sort_order: str, sort_order_asc: bool, sort_order_desc: bool) -> None:
    """\b
    Lists all existing Habits.

    If a Periodicity is given, uses it as a filter.
    If a Sort Order is given, uses it to sort the Habits by the given field.
    """
    with ctx.obj['session_maker']() as session:
        query = (session.query(Habit,
                               func.count(HabitEntry.habit_entry_id).label('total_completions'),
                               func.max(HabitEntry.completion_date).label('most_recent_completion'))
                        .join(HabitEntry, Habit.habit_id == HabitEntry.habit_id, isouter=True)
                        .group_by(Habit.habit_id))

        if periodicity is not None:
            query = query.filter(Habit.periodicity == periodicity)

        target, number_based = get_sort_target(sort_order)
        if number_based and not sort_order_asc and not sort_order_desc:
            sort_order_desc = True

        if target is not None:
            if sort_order_desc:
                query = query.order_by(target.desc())
            else:
                query = query.order_by(target.asc())

        habits = query.all()
        list_habits(habits, extra_headers=['Total Completions', 'Most Recent Completion'])


@analytics.command(name='streak')
@click.option('-i', '--id', 'habit_id', type=int, default=None, help='ID of the Habit that should be searched for. Takes precedence over --name.')
@click.option('-n', '--name', type=str, default=None, help='Name of the Habit that should be searched for.')
@click.option('-p', '--period', 'periodicity', default=None, help='Periodicity of the Habit(s) that should be searched for.', type=click.UNPROCESSED, callback=validate_periodicity)
@click.option('-a', '--active', default=False, is_flag=True, help='Get the longest streak that is currently active', type=bool)
@click.pass_context
def analytics_longest_streak(ctx: Context, habit_id: Optional[int], name: Optional[str], periodicity: Optional[Periodicity], active: bool) -> None:
    """\b
    Find the longest streak of a Habit based on the given parameters.
    Habits are identified either by their ID or their Name.

    If neither an ID nor a Name is given, the Habit with the longest total streak is returned.
    This can additionally be refined by specifying a Periodicity.
    """
    with ctx.obj['session_maker']() as session:
        query = session.query(Habit)

        specific_habit = habit_id is not None or name is not None
        if habit_id is not None:
            query = query.filter(Habit.habit_id == habit_id)
        elif name is not None:
            query = query.filter(Habit.name == name)

        if periodicity is not None:
            query = query.filter(Habit.periodicity == periodicity)

        sort_order = Habit.streak if active else Habit.highest_streak
        query = query.order_by(sort_order.desc())

        habit_with_longest_streak = query.first()

        if habit_with_longest_streak is None:
            colored_print('No Matching Habit found.', TerminalColor.YELLOW)
            return

        streak_value = habit_with_longest_streak.streak if active else habit_with_longest_streak.highest_streak

        if specific_habit:
            colored_print(f"The Habit {habit_with_longest_streak.name} has a{'n active' if active else ' longest'} streak of {streak_value}!", TerminalColor.GREEN)
        else:
            colored_print(f"The Habit with the longest{' active' if active else ''} streak is: {habit_with_longest_streak.name} with a streak of {streak_value}!", TerminalColor.GREEN)


# region Helpers

def get_sort_target(sort: str) -> Tuple[Mapped, bool]:
    """
    Returns the SQLAlchemy Mapped Object that should be used for sorting and whether the target is number-based.
    Number-based targets are sorted in descending order by default.

    :param sort: Sort Order to be used
    :returns Mapped: SQLAlchemy Mapped Object to be used for sorting
    :returns bool: Whether the target is number-based
    """
    target: Mapped
    number_based: bool = False

    if sort == 'ID':
        target = Habit.habit_id
    elif sort == 'Name':
        target = Habit.name
    elif sort == 'Streak':
        target = Habit.streak
        number_based = True
    elif sort == 'HighestStreak':
        target = Habit.highest_streak
        number_based = True
    elif sort == 'Periodicity':
        target = Habit.periodicity
    elif sort == 'CreationDate':
        target = Habit.creation_date
        number_based = True
    elif sort == 'TotalCompletions':
        target = func.count(HabitEntry.habit_entry_id)
        number_based = True
    elif sort == 'MostRecentCompletion':
        target = func.max(HabitEntry.completion_date)
        number_based = True
    else:
        raise NotImplementedError(f'No implementation for sort order {sort}!')

    return target, number_based

# endregion
