"""CRUD operations for the Expense model."""
from datetime import date

from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

from database.config import async_session_maker
from database.crud.categories import user_category_exist_by_id
from database.crud.user_configs import user_config_exist_by_id
from database.crud.users import user_exist_by_id
from database.exceptions import CategoryNotFoundError, ExpenseNotFoundError, UserConfigNotFoundError, UserNotFoundError
from database.models import Expense, User


async def add_expense(
    name: str,
    currency: str,
    amount: float,
    expense_date: date,
    user_tg_id: int,
    category_id: int,
) -> None:
    """Asynchronously adds a new expense to the database.

    Args:
        name (str): The name of the expense.
        currency (str): The currency of the expense.
        amount (float): The amount of the expense.
        expense_date (date): The date of the expense.
        user_tg_id (int): The Telegram user ID associated with the expense.
        category_id (int): The category ID associated with the expense.

    Raises:
        UserNotFoundError: If the user with the given Telegram ID does not exist.
        UserConfigNotFoundError: If the user configuration for the given Telegram ID does not exist.
        CategoryNotFoundError: If the category with the given ID does not exist.
    """
    async with async_session_maker() as session:
        if not await user_exist_by_id(session, user_tg_id):
            raise UserNotFoundError(f"User with id {user_tg_id} not found")
        if not await user_config_exist_by_id(session, user_tg_id):
            raise UserConfigNotFoundError(f"UserConfig for User with id {user_tg_id} not found")
        if not await user_category_exist_by_id(session, category_id):
            raise CategoryNotFoundError(f"Category with id {category_id} not found")

        new_expense = Expense(
            name=name,
            currency=currency,
            amount=amount,
            date=expense_date,
            user_tg_id=user_tg_id,
            category_id=category_id,
        )
        session.add(new_expense)
        await session.commit()
        await session.refresh(new_expense)


async def get_all_expenses_by_tg_id(tg_id: int) -> list[Expense]:
    """Retrieve all expenses associated with a user by their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.

    Returns:
        list[Expense]: A list of Expense objects associated with the user.

    Raises:
        UserNotFoundError: If the user with the given Telegram ID does not exist.
        UserConfigNotFoundError: If the user configuration for the given Telegram ID does not exist.
        ExpenseNotFoundError: If no expenses are found for the user with the given Telegram ID.
    """
    async with async_session_maker() as session:
        if not await user_exist_by_id(session, tg_id):
            raise UserNotFoundError(f"User with id {tg_id} not found")
        if not await user_config_exist_by_id(session, tg_id):
            raise UserConfigNotFoundError(f"UserConfig for User with id {tg_id} not found")
        select_result = await session.execute(
            select(User)
            .options(selectinload(User.expenses))  # noqa: WPS348
            .filter(User.user_tg_id == tg_id),  # noqa: WPS348
        )
        user = select_result.scalars().first()

        if user and user.expenses:
            # Return the list of expenses associated with the user
            return user.expenses
        raise ExpenseNotFoundError(f"No expenses found for user with id {tg_id}")


async def get_all_currencies_used_by_tg_id(tg_id: int) -> list[str] | None:
    """Retrieve a list of distinct currencies used by a user identified by their Telegram ID.

    This asynchronous function queries the database to fetch all unique currencies
    associated with the expenses of a specific user.

    Args:
        tg_id (int): The Telegram ID of the user whose currencies are to be retrieved.

    Returns:
        list[str] | None: A list of unique currency codes (as strings) used by the user,
        or None if no currencies are found.
    """
    async with async_session_maker() as session:
        query = select(Expense.currency).where(Expense.user_tg_id == tg_id).distinct()
        query_result = await session.execute(query)
        return [row[0] for row in query_result.all()]
