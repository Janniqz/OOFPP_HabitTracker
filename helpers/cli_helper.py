from typing import Type, List

from tabulate import tabulate

from classes.orm.habit import Habit


def confirm_action(confirmation_text: str) -> bool:
    """
    Asks for user confirmation and returns the confirmation status.

    :param confirmation_text: Text displayed for the confirmation

    :returns: Confirmation Result
    """
    confirmation = input(confirmation_text)
    return confirmation in ('y', 'yes')


def get_input(prompt_text: str, error_text: str, condition) -> str:
    """
    Function to get user input with specified prompt and condition.
    """
    result = None

    while result is None:
        result = input(prompt_text)
        if not condition(result):
            result = None
            print(error_text)

    return result


def list_habits(habits: List[Type[Habit]]) -> None:
    """
    Lists all Habits in a tabular format.

    :param habits: List of Habits to be displayed
    """
    data = []
    headers = ["ID", "Name", "Current Streak", "Longest Streak", "Periodicity"]

    for habit in habits:
        data.append([habit.habit_id, habit.name, habit.streak, habit.highest_streak, habit.periodicity.name])

    print(tabulate(tabular_data=data, headers=headers))