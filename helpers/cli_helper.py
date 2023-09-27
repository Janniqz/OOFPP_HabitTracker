from typing import Type, List

from tabulate import tabulate

from classes.orm.habit import Habit


def list_habits(habits: List[Type[Habit]]) -> None:
    """
    Prints a formatted table of the given list of habits.
    """
    data = []
    headers = ["ID", "Name", "Current Streak", "Longest Streak", "Periodicity"]

    for habit in habits:
        data.append([habit.habit_id, habit.name, habit.streak, habit.highest_streak, habit.periodicity.name])

    print(tabulate(tabular_data=data, headers=headers))
