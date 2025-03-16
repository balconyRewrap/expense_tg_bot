"""Module contains the business logic for user-related operations."""
from database.crud.categories import add_user_categories as db_add_user_categories
from database.crud.user_configs import add_user_config as db_add_user_config
from database.crud.users import add_user as db_add_user
from database.exceptions import UniqueDublicateError, UserConfigNotFoundError, UserNotFoundError


class UserNotRegisteredError(Exception):
    """Raised when a user is not registered in the database."""


async def add_user(tg_id: int, language: str, currency: str, categories: list[str]) -> None:  # noqa: WPS238, C901
    """Add a new user to the database with the specified configuration and categories.

    Args:
        tg_id (int): The Telegram ID of the user.
        language (str): The preferred language of the user.
        currency (str): The preferred currency of the user.
        categories (list[str]): A list of categories associated with the user.

    Raises:
        UserNotRegisteredError: If the user already exists, the user configuration already exists,
                                the user is not found, or the user configuration is not found.
    """
    try:
        await db_add_user(tg_id)
    except UniqueDublicateError as exception:
        raise UserNotRegisteredError("User with same tg_id exist") from exception

    try:
        await db_add_user_config(tg_id, language, currency)
    except UniqueDublicateError as exception:
        raise UserNotRegisteredError("Config for this user already exist") from exception
    except UserNotFoundError as exception:
        raise UserNotRegisteredError("User not found") from exception

    try:
        await db_add_user_categories(tg_id, categories)
    except UserNotFoundError as exception:
        raise UserNotRegisteredError("User not found") from exception
    except UserConfigNotFoundError as exception:
        raise UserNotRegisteredError("User config not found") from exception
