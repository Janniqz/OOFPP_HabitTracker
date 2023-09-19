from typing import Optional

import click
from click import Group

from classes.validations import validate_habit_name, validate_periodicity
from classes.periodicity import Periodicity


@click.group()
def habit() -> Group:
    pass


@habit.command(name='create')
@click.option('-n', '--name', required=True, prompt=True, help='Name of the Habit to help with identification', type=click.UNPROCESSED, callback=validate_habit_name)
@click.option('-p', '--period', required=True, prompt=True, help='Periodicity in which the Habit should be tracked (d/daily w/weekly)', type=click.UNPROCESSED, callback=validate_periodicity)
def habit_create(name: str, period: Periodicity) -> None:
    """
    Creates a new Habit
    """
    pass


@habit.command(name='delete')
@click.option('-i', '--id', 'habit_id', required=False, help='ID of the Habit that should be searched for. Takes precedence over --name.', type=int)
@click.option('-n', '--name', required=False, help='Name of the Habit to help with identification', type=str)
def habit_delete(habit_id: Optional[int], name: Optional[str]) -> None:
    """
    Deletes an existing Habit.
    Unless a Backup of the Database exists this is irreversible!
    """
    pass


@habit.command(name='modify')
@click.option('-i', '--id', 'habit_id', required=True, prompt=True, help='ID of the Habit that should be modified', type=int, default=None)
@click.option('-n', '--name', required=False, help='Updated Name for the Habit', type=click.UNPROCESSED, callback=validate_habit_name)
@click.option('-p', '--period', required=False, help='Updated Periodicity for the Habit (d/daily w/weekly)', type=click.UNPROCESSED, callback=validate_periodicity)
def habit_modify() -> None:
    """
    Modify a Habit with the provided details.
    Not providing a name / period will keep their current values.
    """
    pass


@habit.command(name='complete')
@click.option('-i', '--id', 'habit_id', type=int, default=None, help='ID of the Habit that should be searched for. Takes precedence over --name.')
@click.option('-n', '--name', required=False, prompt=True, help='Name of the Habit to help with identification', type=str)
def habit_complete(habit_id: Optional[int], name: Optional[str]) -> None:
    """
    Completes a habit via either its ID or name.
    If both are given, the ID takes precedence.
    """
    pass
