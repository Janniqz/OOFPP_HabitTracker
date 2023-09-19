from typing import Union

import click

from classes.periodicity import Periodicity


def validate_periodicity(ctx, param, value: Union[str, Periodicity]) -> Periodicity:
    if isinstance(value, Periodicity):
        return value

    try:
        periodicity = Periodicity.from_str(value)
        return periodicity
    except NotImplementedError:
        raise click.BadParameter("Period must be one of: d/daily w/weekly")


def validate_habit_name(ctx, param, value: str) -> str:
    if len(value) == 0 or value.isspace():
        raise click.BadParameter("Name needs to include at least one non-whitespace Character!")
    return value
