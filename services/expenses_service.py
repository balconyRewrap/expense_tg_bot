"""Module contains the business logic for the expenses service."""
from collections import defaultdict
from datetime import date, timedelta
from enum import Enum

from dateutil.relativedelta import relativedelta

from database.crud import expenses as expenses_crud
from database.exceptions import CategoryNotFoundError, ExpenseNotFoundError, UserConfigNotFoundError, UserNotFoundError
from database.models import Expense


class ExpenseNotAddedError(Exception):
    """Raised when an expense is not added to the database."""


class StatisticsNotGeneratedError(Exception):
    """Raised when statistics are not generated."""


class ExpensePeriod(Enum):
    """Enum class representing different periods for categorizing expenses.

    Attributes:
        DAY (str): Represents a single day period.
        WEEK (str): Represents a weekly period.
        MONTH (str): Represents a monthly period.
        YEAR (str): Represents a yearly period.
        ALL (str): Represents all-time expenses.
    """

    # WPS ignore, that it is a Enum. It is a valid use case
    DAY = "day_period"  # noqa: WPS115
    WEEK = "week_period"  # noqa: WPS115
    MONTH = "month_period"  # noqa: WPS115
    YEAR = "year_period"  # noqa: WPS115
    ALL = "all_time_period"  # noqa: WPS115


type CustomPeriod = tuple[date, date]

ALL_CATEGORIES_ID = -1


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


async def get_expenses_by_category_ids_by_period(
    tg_id: int,
    category_ids: list[int],
    period: ExpensePeriod | None = None,
    custom_period: CustomPeriod | None = None,
) -> dict[int, list[Expense]] | None:
    """Retrieve expenses grouped by category IDs for a given user within a specified period.

    This function fetches all expenses for a user identified by their Telegram ID (`tg_id`),
    filters them by a specified period (either a predefined `ExpensePeriod` or a custom
    `CustomPeriod`), and groups the filtered expenses by their category IDs.

    Args:
        tg_id (int): The Telegram ID of the user whose expenses are being retrieved.
        category_ids (list[int]): A list of category IDs to group the expenses by.
        period (ExpensePeriod | None, optional): A predefined period to filter expenses.
            If not provided, `custom_period` must be specified.
        custom_period (CustomPeriod | None, optional): A custom period to filter expenses.
            If not provided, `period` must be specified.

    Returns:
        dict[int, list[Expense]] | None: A dictionary where the keys are category IDs
            and the values are lists of `Expense` objects for that category. Returns
            `None` if no period is specified or if no expenses are found.

    Note:
        Either `period` or `custom_period` must be provided. If both are `None`, the
        function will return `None`.
    """
    if not period and not custom_period:
        return None

    if not custom_period:
        custom_period = _get_period(period)
        if not custom_period:
            return None
    try:
        expenses = await expenses_crud.get_all_expenses_by_tg_id(tg_id)
    except ExpenseNotFoundError:
        return None

    filtered_expenses_by_period = _filter_expenses_by_period(expenses, custom_period)
    return _filter_expenses_by_category_ids(filtered_expenses_by_period, category_ids)


def _get_period(period: ExpensePeriod | None) -> CustomPeriod | None:
    """Determine the custom period based on the provided expense period.

    Args:
        period (ExpensePeriod | None): The expense period to calculate the custom period from.
            If None, no period is provided.

    Returns:
        CustomPeriod | None: A tuple containing the start date and today's date if the period is valid.
            Returns None if the period is not provided or invalid.
    """
    if not period:
        return None
    start_date = _get_start_date(period)
    if not start_date:
        return None
    return (start_date, date.today())


def _filter_expenses_by_period(expenses: list[Expense], period: CustomPeriod) -> list[Expense]:
    """Filter a list of expenses to include only those that fall within a specified date range.

    Args:
        expenses (list[Expense]): A list of Expense objects to be filtered.
        period (CustomPeriod): A tuple containing the start and end dates (start_date, end_date)
            that define the filtering period.

    Returns:
        list[Expense]: A list of Expense objects that have a date within the specified period.
    """
    start_date, end_date = period
    # It works, pyright doesn't understand SQLALCHEMY objects
    return [expense for expense in expenses if start_date <= expense.date <= end_date]  # pyright: ignore[reportGeneralTypeIssues]


def _filter_expenses_by_category_ids(
    expenses: list[Expense],
    category_ids: list[int],
) -> dict[int, list[Expense]]:
    """Filter and group a list of expenses by their category IDs.

    Args:
        expenses (list[Expense]): A list of Expense objects to be filtered.
        category_ids (list[int]): A list of category IDs to filter the expenses by.

    Returns:
        dict[int, list[Expense]]: A dictionary where the keys are category IDs
        and the values are lists of Expense objects that belong to those categories.
    """
    grouped_expenses = defaultdict(list)
    for expense in expenses:
        if expense.category_id in category_ids:
            grouped_expenses[expense.category_id].append(expense)
        if ALL_CATEGORIES_ID in category_ids:
            grouped_expenses[ALL_CATEGORIES_ID].append(expense)
    return dict(grouped_expenses)


# no, here so many returns is okay, because they have the same simple logic.
def _get_start_date(period: ExpensePeriod) -> date | None:  # noqa: WPS212
    """Calculate the start date based on the given expense period.

    Args:
        period (ExpensePeriod): The period for which the start date is to be calculated.
            - ExpensePeriod.DAY: Returns the date one day before today.
            - ExpensePeriod.WEEK: Returns the date one week before today.
            - ExpensePeriod.MONTH: Returns the date one month before today.
            - ExpensePeriod.YEAR: Returns the date one year before today.
            - ExpensePeriod.ALL: Returns the earliest possible date (date.min).

    Returns:
        date | None: The calculated start date for the given period, or None if the period is invalid.
    """
    today = date.today()

    if period == ExpensePeriod.DAY:
        return today - timedelta(days=1)
    if period == ExpensePeriod.WEEK:
        return today - timedelta(weeks=1)
    if period == ExpensePeriod.MONTH:
        return today - relativedelta(months=1)
    if period == ExpensePeriod.YEAR:
        return today - relativedelta(years=1)
    if period == ExpensePeriod.ALL:
        return date.min

    return None
