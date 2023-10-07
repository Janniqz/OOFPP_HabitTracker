import pytest
from click.testing import CliRunner

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from classes.orm.base import Base
from modules.habit import habit

# Set up the SQLAlchemy session
engine = create_engine('sqlite:///:memory:', echo=True)
session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Initialize your database tables
Base.metadata.create_all(bind=engine)


@pytest.fixture
def runner():
    return CliRunner()


def test_create(runner):
    result = runner.invoke(habit, ['create'], obj={'session_maker': session_maker}, input='Test Habit\nd\n')
    assert 'Habit "Test Habit" has been created with a Daily Periodicity!' in result.output


def test_complete(runner):
    result = runner.invoke(habit, ['complete'], obj={'session_maker': session_maker}, input='Test Habit')
    assert 'You have completed Habit "Test Habit"! (Streak: 1)' in result.output


def test_modify(runner):
    result = runner.invoke(habit, ['modify'], obj={'session_maker': session_maker}, input='1\nY\nChanged Habit\nN')
    assert 'Habit has been updated!' in result.output


def test_delete(runner):
    result = runner.invoke(habit, ['delete'], obj={'session_maker': session_maker}, input='Changed Habit\nY')
    assert 'Habit "Changed Habit" has been deleted!' in result.output
