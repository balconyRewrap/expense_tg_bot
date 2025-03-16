"""Module contains the business logic for the expenses service."""
from datetime import date

from database.crud.expenses import add_expense as db_add_expense
from database.exceptions import CategoryNotFoundError, UserConfigNotFoundError, UserNotFoundError


class ExpenseNotAddedError(Exception):
    """Raised when an expense is not added to the database."""


async def add_expense(name: str, currency: str, amount: float, user_tg_id: int, category_id: int) -> None:
    """Asynchronously adds a new expense to the database.

    Args:
        name (str): The name of the expense.
        currency (str): The currency of the expense.
        amount (float): The amount of the expense.
        user_tg_id (int): The Telegram user ID associated with the expense.
        category_id (int): The category ID associated with the expense.

    Raises:
        ExpenseNotAddedError: If the expense is not added to the database.
    """
    try:
        await db_add_expense(name, currency, amount, date.today(), user_tg_id, category_id)
    except (UserNotFoundError, UserConfigNotFoundError, CategoryNotFoundError) as exception:
        raise ExpenseNotAddedError("Expenses not added to DB") from exception
