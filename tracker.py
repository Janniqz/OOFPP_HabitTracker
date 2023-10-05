import click

from classes.orm.base import Base
from classes.orm.habit import Habit  # noqa
from classes.orm.habit_entry import HabitEntry  # noqa

from modules.analytics import analytics
from modules.habit import habit
from sqlalchemy import create_engine


@click.group()
@click.pass_context
def cli(ctx):
    """\b
    Application Base.

    The --help argument can be used to get more information about specific commands.
    Please choose any of the following modules:
    """
    if ctx.invoked_subcommand is None:
        return

    ctx.ensure_object(dict)
    ctx.obj['connection'] = create_engine("sqlite:///habits.sqlite")
    Base.metadata.create_all(ctx.obj['connection'])
    pass


if __name__ == '__main__':
    cli.add_command(analytics)
    cli.add_command(habit)
    cli()
