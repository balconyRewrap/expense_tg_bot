"""Module contains the business logic for the expenses service."""
from datetime import date

from database.crud import expenses as expenses_crud
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
        await expenses_crud.add_expense(name, currency, amount, date.today(), user_tg_id, category_id)
    except (UserNotFoundError, UserConfigNotFoundError, CategoryNotFoundError) as exception:
        raise ExpenseNotAddedError("Expenses not added to DB") from exception


async def get_all_currencies_used_by_tg_id(tg_id: int) -> list[str] | None:
    """Retrieve all currencies used in expenses by a user based on their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.

    Returns:
        list[str] | None: A list of currency codes used in expenses by the user, or None if the user is not found.

    Raises:
        UserNotFoundError: If the user is not found.
    """
    try:
        return await expenses_crud.get_all_currencies_used_by_tg_id(tg_id)
    except UserNotFoundError:
        return None
