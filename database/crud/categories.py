"""CRUD operations for the Category model."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import delete, select

from database.config import async_session_maker
from database.crud.user_configs import user_config_exist_by_id
from database.crud.users import user_exist_by_id
from database.exceptions import CategoryNotFoundError, UserConfigNotFoundError, UserNotFoundError
from database.models import Category, User, UserConfig


async def add_user_categories(tg_id: int, categories: list[str]) -> None:
    """Add a list of categories for a user.

    Args:
        tg_id (int): The Telegram ID of the user.
        categories (list[str]): A list of category names to add.

    Raises:
        UserNotFoundError: If the user with the given Telegram ID does not exist.
        UserConfigNotFoundError: If the user configuration for the given Telegram ID does not exist.
    """
    async with async_session_maker() as session:
        if not await user_exist_by_id(session, tg_id):
            raise UserNotFoundError(f"User with id {tg_id} not found")
        if not await user_config_exist_by_id(session, tg_id):
            raise UserConfigNotFoundError(f"UserConfig for User with id {tg_id} not found")

        for category in categories:
            await _add_user_category(session, tg_id, category)


async def get_user_categories_by_tg_id(tg_id: int) -> list[Category]:
    """Retrieve the list of categories associated with a user by their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user.

    Returns:
        list[Category]: A list of Category objects associated with the user.

    Raises:
        UserNotFoundError: If the user with the given Telegram ID does not exist.
        UserConfigNotFoundError: If the user configuration for the given Telegram ID does not exist.
        CategoryNotFoundError: If no categories are found for the user.
    """
    async with async_session_maker() as session:
        if not await user_exist_by_id(session, tg_id):
            raise UserNotFoundError(f"User with id {tg_id} not found")
        if not await user_config_exist_by_id(session, tg_id):
            raise UserConfigNotFoundError(f"UserConfig for User with id {tg_id} not found")
        select_result = await session.execute(
            select(User)
            .options(selectinload(User.config).selectinload(UserConfig.categories))  # noqa: WPS348
            .filter(User.user_tg_id == tg_id),  # noqa: WPS348
        )
        user = select_result.scalars().first()

        if user and user.config and user.config.categories:
            # Return the list of categories associated with the user
            return user.config.categories
        raise CategoryNotFoundError(f"No categories found for user with id {tg_id}")


async def remove_user_category_by_id(tg_id: int, category_id: int) -> None:
    """Remove a category from a user's list of categories.

    Args:
        tg_id (int): The Telegram ID of the user.
        category_id (int): The ID of the category to remove.

    Raises:
        UserNotFoundError: If the user with the given Telegram ID does not exist.
        UserConfigNotFoundError: If the user configuration for the given Telegram ID does not exist.
        CategoryNotFoundError: If the category with the given ID does not
        Exception: Any other exception, that can raise during the deleting.
    """
    async with async_session_maker() as session:
        if not await user_exist_by_id(session, tg_id):
            raise UserNotFoundError(f"User with id {tg_id} not found")
        if not await user_config_exist_by_id(session, tg_id):
            raise UserConfigNotFoundError(f"UserConfig for User with id {tg_id} not found")
        if not await user_category_exist_by_id(session, category_id):
            raise CategoryNotFoundError(f"Category with id {category_id} not found")
        try:
            await session.execute(delete(Category).where(Category.id == category_id))
            await session.commit()
        except Exception:
            await session.rollback()  # noqa: ASYNC120
            raise


# name of this function is bool-like.
async def user_category_exist_by_id(session: AsyncSession, category_id: int) -> bool:  # noqa: FNE005
    """Check if a category exists in the database.

    Args:
        session (AsyncSession): The SQLAlchemy async session to use for the query.
        category_id (int): The ID of the category to check.

    Returns:
        bool: True if the category exists, False otherwise.
    """
    select_result = await session.execute(select(Category).filter_by(id=category_id))
    category = select_result.scalars().first()
    return bool(category)


async def _add_user_category(session: AsyncSession, user_tg_id: int, name: str) -> None:
    """Asynchronously adds a new category for a user.

    Args:
        session (AsyncSession): The database session to use for the operation.
        user_tg_id (int): The Telegram ID of the user.
        name (str): The name of the category to add.
    """
    new_category = Category(name=name, config_id=user_tg_id)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
