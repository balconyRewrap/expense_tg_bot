"""Services for user configuration operations."""
import contextlib

from database.crud.categories import add_user_categories, get_user_categories_by_tg_id, remove_user_category_by_id
from database.crud.user_configs import change_user_config_language, get_user_config_by_id
from database.exceptions import CategoryNotFoundError, UserConfigNotFoundError, UserNotFoundError

type CategoryData = tuple[str, int]


class UserConfigNotChangedError(Exception):
    """Raised when a user configuration is not changed."""


# name of this function is bool-like.
async def user_config_exist_by_tg_id(tg_id: int) -> bool:  # noqa: FNE005
    """Check if a user configuration exists based on their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.

    Returns:
        bool: True if the user configuration exists, False otherwise.
    """
    try:
        await get_user_config_by_id(tg_id)
    except UserConfigNotFoundError:
        return False
    return True


async def get_currency_by_tg_id(tg_id: int) -> str | None:
    """Retrieve the currency preference for a user based on their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.

    Returns:
        str | None: The currency preference of the user if found, otherwise None.

    Raises:
        UserConfigNotFoundError: If the user configuration is not found.
    """
    try:
        user_config = await get_user_config_by_id(tg_id)
    except UserConfigNotFoundError:
        return None
    return str(user_config.currency)


async def get_language_by_tg_id(tg_id: int) -> str | None:
    """Retrieve the language preference for a user based on their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.

    Returns:
        str | None: The language preference of the user if found, otherwise None.

    Raises:
        UserConfigNotFoundError: If the user configuration is not found.
    """
    try:
        user_config = await get_user_config_by_id(tg_id)
    except UserConfigNotFoundError:
        return None
    return str(user_config.language)


async def set_language_by_tg_id(tg_id: int, language: str) -> None:
    """Set the language preference for a user identified by their Telegram ID.

    This function attempts to change the language setting for a user in the user configuration.
    If the user configuration is not found, the exception is suppressed.

    Args:
        tg_id (int): The Telegram ID of the user.
        language (str): The language code to set for the user.
    """
    with contextlib.suppress(UserConfigNotFoundError):
        await change_user_config_language(tg_id, language)


async def add_user_expenses_categories(tg_id: int, categories: list[str]) -> None:
    """Add expense categories for a user based on their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.
        categories (list[str]): A list of category names to add for the user.

    Raises:
        UserConfigNotChangedError: If the user configuration is not changed.
    """
    try:
        await add_user_categories(tg_id, categories)
    except UserNotFoundError as exception:
        raise UserConfigNotChangedError("User not found") from exception
    except UserConfigNotFoundError as exception:
        raise UserConfigNotChangedError("User config not found") from exception


async def remove_user_expenses_category(tg_id: int, category_id: int) -> None:
    """Remove an expense category for a user based on their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.
        category_id (int): The ID of category to remove.

    Raises:
        UserConfigNotChangedError: If the user configuration is not changed.
    """
    try:
        await remove_user_category_by_id(tg_id, category_id)
    except (UserNotFoundError, UserConfigNotFoundError, CategoryNotFoundError) as exception:
        raise UserConfigNotChangedError("User not found") from exception
    except Exception as exception:
        raise UserConfigNotChangedError("Unknown error") from exception


async def get_user_expenses_categories(tg_id: int) -> list[CategoryData] | None:
    """Fetch the expense categories for a user based on their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.

    Returns:
        list[CategoryData] | None: A list of CategoryData tuples containing the category name and ID,
        or None if the user or categories are not found.

    Raises:
        UserNotFoundError: If the user is not found.
        UserConfigNotFoundError: If the user configuration is not found.
        CategoryNotFoundError: If the categories are not found.
    """
    try:
        user_categories = await get_user_categories_by_tg_id(tg_id)
    except (UserNotFoundError, UserConfigNotFoundError, CategoryNotFoundError):
        return None
    return [(str(category.name), int(category.id)) for category in user_categories]  # pyright: ignore[reportArgumentType]
