from typing import Optional

import click

from classes.periodicity import Periodicity


def validate_periodicity(*args) -> Optional[Periodicity]:
    """
    Validate Habit Periodicity's.
    Attempts to cast retrieve a Periodicity instance if the passed value is a string.

    :param ctx: Click Context
    :param param: Parameter to be validated
    :param value: Periodicity to be validated

    :returns: Validated Value
    :raises click.BadParameter: Invalid Periodicity value was used
    """
    str_value: str
    if len(args) == 1 and isinstance(args[0], str):
        str_value = args[0]
    elif len(args) == 3:
        if isinstance(args[2], Periodicity):
            return args[2]
        str_value = args[2]
    else:
        raise click.BadParameter("Invalid Usage of validate_periodicity!")

    try:
        periodicity = Periodicity.from_str(str_value)
        return periodicity
    except NotImplementedError:
        raise click.BadParameter("Period must be one of: d/daily w/weekly")


def validate_habit_name(*args) -> Optional[str]:
    """
    Validates Habit Names passed as command-line arguments.
    Habit names must consist of at least 1 character that is not whitespace.

    :param ctx: Click Context
    :param param: Parameter to be validated
    :param value: Habit Name to be validated

    :returns: Validated Value
    :raises click.BadParameter: Empty String was passed
    """
    str_value: str
    if len(args) == 1 and isinstance(args[0], str):
        str_value = args[0]
    elif len(args) == 3:
        str_value = args[2]
    else:
        raise click.BadParameter("Invalid Usage of validate_periodicity!")

    if str_value is not None and (len(str_value) == 0 or str_value.isspace()):
        raise click.BadParameter("Name needs to include at least one non-whitespace Character!")
    return str_value
