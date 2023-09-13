import click
from click import Command, Group


@click.group()
def analytics() -> Group:
    pass


@analytics.command(name='list')
def analytics_list() -> Command:
    pass


@analytics.command(name='streak')
def analytics_streak() -> Command:
    pass