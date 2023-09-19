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
