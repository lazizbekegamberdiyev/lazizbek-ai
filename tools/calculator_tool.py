from tools.calculator import calculate


def calculator(expression: str) -> float | str:
    """
    Calculate a mathematical expression safely.

    Args:
        expression: A mathematical expression such as
                    "15 * 2000000 / 100".

    Returns:
        The calculated result or an error message.
    """
    return calculate(expression)
