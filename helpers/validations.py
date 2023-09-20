from typing import Union, Optional

import click
from click import Context

from classes.periodicity import Periodicity


def validate_periodicity(ctx: Context, param, value: Union[str, Periodicity]) -> Optional[Periodicity]:
    """
    Validate Habit Periodicity's.
    Attempts to cast retrieve a Periodicity instance if the passed value is a string.

    :param ctx: Click Context
    :param param: Parameter to be validated
    :param value: Periodicity to be validated

    :returns: Validated Value
    :raises click.BadParameter: Invalid Periodicity value was used
    """
    if isinstance(value, Periodicity):
        return value

    try:
        periodicity = Periodicity.from_str(value)
        return periodicity
    except NotImplementedError:
        raise click.BadParameter("Period must be one of: d/daily w/weekly")


def validate_habit_name(ctx: Context, param, value: str) -> Optional[str]:
    """
    Validates Habit Names passed as command-line arguments.
    Habit names must consist of at least 1 character that is not whitespace.

    :param ctx: Click Context
    :param param: Parameter to be validated
    :param value: Habit Name to be validated

    :returns: Validated Value
    :raises click.BadParameter: Empty String was passed
    """
    if value is not None and (len(value) == 0 or value.isspace()):
        raise click.BadParameter("Name needs to include at least one non-whitespace Character!")
    return value
