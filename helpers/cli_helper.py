from typing import Type, List, Optional, Tuple

import click
from sqlalchemy import Row
from tabulate import tabulate

from classes.helpers.terminal_options import TerminalColor, TerminalFormat
from classes.orm.habit import Habit


def list_habits(habits: List[Type[Habit] | Row], extra_headers: Optional[List[str]] = None) -> None:
    """
    Prints a formatted table of the given list of habits.

    :param habits: List of Habits to be printed
    :param extra_headers: List of extra headers to be added to the table
    """
    data = []
    headers = ["ID", "Name", "Current Streak", "Longest Streak", "Periodicity"]
    if extra_headers is not None:
        headers.extend(extra_headers)

    if isinstance(habits[0], Habit):
        for habit in habits:
            data.append([habit.habit_id, habit.name, habit.streak, habit.highest_streak, habit.periodicity.name])
    elif isinstance(habits[0], Row):
        for habit in habits:
            habit_data = []
            for field in habit:
                if isinstance(field, Habit):
                    habit_data.extend([field.habit_id, field.name, field.streak, field.highest_streak, field.periodicity.name])
                else:
                    habit_data.append(field)
            data.append(habit_data)

    print(tabulate(tabular_data=data, headers=headers))


def colored_print(message: str, color: Optional[TerminalColor] = None, format_: Optional[TerminalFormat] = None) -> None:
    """
    Prints an error message in a formatted way.

    :param message: Message to be printed
    :param color: Color of the message
    :param format_: Format of the message
    """
    color = color.value if color is not None else ''
    format_ = format_.value if format_ is not None else ''

    click.echo(message=f'{color}{format_}{message}\033[0m', color=True)
