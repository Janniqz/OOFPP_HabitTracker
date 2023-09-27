from typing import Optional, List, Type

import click
from click import Context
from sqlalchemy import Select
from sqlalchemy.orm import Session

from classes.helpers.terminal_options import TerminalColor
from classes.orm.habit import Habit
from classes.periodicity import Periodicity
from helpers.cli_helper import colored_print, list_habits
from helpers.validations import validate_habit_name, validate_periodicity


@click.group(invoke_without_command=True)
@click.pass_context
def habit(ctx: Context) -> None:
    if ctx.invoked_subcommand is not None:
        return

    habits: List[Type[Habit]]
    with Session(ctx.obj['connection']) as session:
        statement: Select
        habits = session.query(Habit).all()

        list_habits(habits)


@habit.command(name='create')
@click.option('-n', '--name', 'habit_name', required=True, prompt=True, help='Name of the Habit to help with identification', type=click.UNPROCESSED, callback=validate_habit_name)
@click.option('-p', '--period', required=True, prompt=True, help='Periodicity in which the Habit should be tracked (d/daily w/weekly)', type=click.UNPROCESSED, callback=validate_periodicity)
@click.pass_context
def habit_create(ctx: Context, habit_name: str, period: Periodicity) -> None:
    """\b
    Creates a new Habit
    """
    with Session(ctx.obj['connection']) as session:
        if Habit.exists(session, habit_name):
            colored_print(f'ERROR: Habit "{habit_name}" already exists!', TerminalColor.RED)
            return

        Habit.create(session, habit_name, period)
        colored_print(f'Habit "{habit_name}" has been created with a {period.name} Periodicity!', TerminalColor.GREEN)


@habit.command(name='delete')
@click.option('-i', '--id', 'habit_id', required=False, help='ID of the Habit that should be searched for. Takes precedence over --name.', type=int)
@click.option('-n', '--name', 'habit_name', required=False, help='Name of the Habit to help with identification', type=str)
@click.pass_context
def habit_delete(ctx: Context, habit_id: Optional[int], habit_name: Optional[str]) -> None:
    """\b
    Deletes an existing Habit.
    Unless a Backup of the Database exists this is irreversible!
    """
    if habit_id is None and not habit_name_condition(habit_name):
        habit_name = click.prompt('Name', type=click.UNPROCESSED, value_proc=validate_habit_name)

    with Session(ctx.obj['connection']) as session:
        target_habit = Habit.get(session, habit_id, habit_name)
        if target_habit is None:
            if habit_id is not None:
                colored_print(f'No Habit with ID {habit_id} exists!', TerminalColor.YELLOW)
            else:
                colored_print(f'No Habit with Name {habit_name} exists!', TerminalColor.YELLOW)
            return

        click.confirm(f'Are you sure you want to delete the Habit \"{target_habit.name}\"?', abort=True)

        target_habit.delete(session)
        colored_print(f'Habit \"{target_habit.name}\" has been deleted!', TerminalColor.GREEN)


@habit.command(name='modify')
@click.option('-i', '--id', 'habit_id', required=True, prompt=True, help='ID of the Habit that should be modified', type=int)
@click.option('-n', '--name', 'habit_name', required=False, help='Updated Name for the Habit', type=click.UNPROCESSED, default=None, callback=validate_habit_name)
@click.option('-p', '--period', required=False, help='Updated Periodicity for the Habit (d/daily w/weekly)', type=click.UNPROCESSED, default=None, callback=validate_periodicity)
@click.pass_context
def habit_modify(ctx: Context, habit_id: int, habit_name: Optional[str], period: Optional[Periodicity]) -> None:
    """\b
    Modify a Habit with the provided details.
    Not providing a name / period will keep their current values.

    NOTE: Changing the Periodicity might end your current Streak!
    """
    with Session(ctx.obj['connection']) as session:
        target_habit = Habit.get(session, habit_id)
        if target_habit is None:
            colored_print(f'ERROR: No Habit with ID {habit_id} found!', TerminalColor.RED)
            return

        if habit_name is None and period is None:
            if click.confirm('Should the Habit name be changed?'):
                habit_name = click.prompt('Name', type=click.UNPROCESSED, value_proc=validate_habit_name)

            if click.confirm('Should the Habit Periodicity be changed?'):
                period = click.prompt('Periodicity (d/daily w/weekly)', type=click.UNPROCESSED, value_proc=validate_periodicity)

        if habit_name is None and period is None:
            colored_print('No fields to change have been passed! Cancelling!', TerminalColor.YELLOW)
            return

        target_habit.update(session, habit_name, period)


@habit.command(name='complete')
@click.option('-i', '--id', 'habit_id', type=int, default=None, help='ID of the Habit that should be searched for. Takes precedence over --name.')
@click.option('-n', '--name', 'habit_name', required=False, prompt=True, help='Name of the Habit to help with identification', type=str)
@click.pass_context
def habit_complete(ctx: Context, habit_id: Optional[int], habit_name: Optional[str]) -> None:
    """\b
    Completes a habit via either its ID or name.
    If both are given, the ID takes precedence.
    """
    if habit_id is None and not habit_name_condition(habit_name):
        habit_name = click.prompt('Name', type=click.UNPROCESSED, value_proc=validate_habit_name)

    with Session(ctx.obj['connection']) as session:
        target_habit = Habit.get(session, habit_id, habit_name)
        if target_habit is not None:
            target_habit.complete(session)


# region Helpers


def habit_name_condition(input_string: str) -> bool:
    return input_string is not None and not input_string.isspace() and len(input_string) != 0


# endregion
