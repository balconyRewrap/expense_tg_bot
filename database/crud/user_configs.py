"""CRUD operations for user configurations in the database."""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from database.config import async_session_maker
from database.crud.users import user_exist_by_id
from database.exceptions import UniqueDublicateError, UserConfigNotFoundError, UserNotFoundError
from database.models import UserConfig


async def add_user_config(tg_id: int, language: str, currency: str) -> None:
    """Asynchronously adds a user configuration to the database.

    This function adds a new user configuration for a given Telegram user ID, language, and currency.
    If the user does not exist, it raises a UserNotFoundError. If there is an integrity error
    (such as a unique constraint violation), it raises a UniqueDublicateError.

    Args:
        tg_id (int): The Telegram user ID.
        language (str): The preferred language of the user.
        currency (str): The preferred currency of the user.

    Raises:
        UserNotFoundError: If the user with the given Telegram ID does not exist.
        UniqueDublicateError: If there is an integrity error while adding the user configuration.
    """
    async with async_session_maker() as session:
        if not await user_exist_by_id(session, tg_id):
            raise UserNotFoundError(f"User with id {tg_id} not found")
        new_user_config = UserConfig(user_tg_id=tg_id, language=language, currency=currency)
        try:
            session.add(new_user_config)
            await session.commit()
        except IntegrityError as exception:
            await session.rollback()  # noqa: ASYNC120
            raise UniqueDublicateError("Failed to add user configuration due to integrity error") from exception
        await session.refresh(new_user_config)


async def change_user_config_language(tg_id: int, new_language: str) -> None:
    """Change the language preference of a user configuration.

    This function updates the language preference of a user configuration based on the Telegram user ID.

    Args:
        tg_id (int): The Telegram user ID.
        new_language (str): The new language preference.

    Raises:
        UserConfigNotFoundError: If the user configuration is not found.
    """
    async with async_session_maker() as session:
        select_result = await session.execute(select(UserConfig).filter_by(user_tg_id=tg_id))
        user_config = select_result.scalars().first()
        if not user_config:
            raise UserConfigNotFoundError(f"UserConfig for User with id {tg_id} not found")
        user_config.language = new_language  # pyright: ignore[reportAttributeAccessIssue]
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def change_user_config_currency(tg_id: int, new_currency: str) -> None:
    """Change the currency preference of a user configuration.

    This function updates the currency preference of a user configuration based on the Telegram user ID.

    Args:
        tg_id (int): The Telegram user ID.
        new_currency (str): The new currency preference.

    Raises:
        UserConfigNotFoundError: If the user configuration is not found.
    """
    async with async_session_maker() as session:
        select_result = await session.execute(select(UserConfig).filter_by(user_tg_id=tg_id))
        user_config = select_result.scalars().first()
        if not user_config:
            raise UserConfigNotFoundError(f"UserConfig for User with id {tg_id} not found")
        user_config.currency = new_currency  # pyright: ignore[reportAttributeAccessIssue]
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_user_config_by_id(tg_id: int) -> UserConfig:
    """Retrieve the user configuration by user Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.

    Returns:
        UserConfig: The configuration settings of the user.

    Raises:
        UserConfigNotFoundError: If no configuration is found for the given user ID.
    """
    async with async_session_maker() as session:
        select_result = await session.execute(select(UserConfig).filter_by(user_tg_id=tg_id))
        user_config = select_result.scalars().first()
        if not user_config:
            raise UserConfigNotFoundError(f"UserConfig for User with id {tg_id} not found")
        return user_config


# name of this function is bool-like.
async def user_config_exist_by_id(session: AsyncSession, tg_id: int) -> bool:  # noqa: FNE005
    """Check if a user configuration exists in the database.

    This asynchronous function queries the database to determine if a user configuration
    exists for a given Telegram user ID.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session to use for the query.
        tg_id (int): The Telegram user ID to check for an existing configuration.

    Returns:
        bool: True if a user configuration exists for the given Telegram user ID, False otherwise.
    """
    select_result = await session.execute(select(UserConfig).filter_by(user_tg_id=tg_id))
    user_config = select_result.scalars().first()
    return bool(user_config)
