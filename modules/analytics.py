from typing import Optional

import click
from click import Group, Context

from classes.periodicity import Periodicity
from helpers.validations import validate_periodicity


@click.group()
def analytics() -> Group:
    """\b
    Command Group related to Habit Analytics
    """
    pass


@analytics.command(name='list')
@click.option('-p', '--period', 'periodicity', default=None, help='Periodicity of the Habit(s) that should be searched for.', type=click.UNPROCESSED, callback=validate_periodicity)
@click.pass_context
def analytics_list(ctx: Context, periodicity: Optional[Periodicity]) -> None:
    """\b
    Lists all existing Habits.
    If a Periodicity is given, uses it as a filter.
    """
    pass


@analytics.command(name='streak')
@click.option('-i', '--id', 'habit_id', type=int, default=None, help='ID of the Habit that should be searched for. Takes precedence over --name.')
@click.option('-n', '--name', type=str, default=None, help='Name of the Habit that should be searched for.')
@click.option('-p', '--period', 'periodicity', default=None, help='Periodicity of the Habit(s) that should be searched for.', type=click.UNPROCESSED, callback=validate_periodicity)
@click.option('-a', '--active', help='Get the longest streak that is currently active', type=bool)
@click.pass_context
def analytics_longest_streak(ctx: Context, habit_id: Optional[int], name: Optional[str], periodicity: Optional[Periodicity]) -> None:
    """\b
    Find the longest streak of a Habit based on the given parameters.
    Habits are identified either by their ID or their Name.

    If neither an ID nor a Name is given, the Habit with the longest total streak is returned.
    This can additionally be refined by specifying a Periodicity.
    """
    pass
