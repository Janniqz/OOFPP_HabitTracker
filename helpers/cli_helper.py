from typing import Type, List, Optional

import click
from tabulate import tabulate

from classes.helpers.terminal_options import TerminalColor, TerminalFormat
from classes.orm.habit import Habit


def list_habits(habits: List[Type[Habit]]) -> None:
    """
    Prints a formatted table of the given list of habits.

    :param habits: List of Habits to be printed
    """
    data = []
    headers = ["ID", "Name", "Current Streak", "Longest Streak", "Periodicity"]

    for habit in habits:
        data.append([habit.habit_id, habit.name, habit.streak, habit.highest_streak, habit.periodicity.name])

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

    click.echo(f'{color}{format_}{message}\033[0m', color=True)
