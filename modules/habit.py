import click
from click import Command, Group


@click.group()
def habit() -> Group:
    pass


@habit.command(name='create')
def habit_create() -> Command:
    pass


@habit.command(name='delete')
def habit_delete() -> Command:
    pass


@habit.command(name='modify')
def habit_modify() -> Command:
    pass


@habit.command(name='complete')
def habit_complete() -> Command:
    pass
