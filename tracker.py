import click
import sqlite3

from modules.analytics import analytics
from modules.habit import habit


@click.group()
def cli():
    pass


if __name__ == '__main__':
    cli.add_command(analytics)
    cli.add_command(habit)
    cli()
