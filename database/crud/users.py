"""CRUD operations for the users table in the database."""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from database.config import async_session_maker
from database.database_utils import is_unique_error
from database.exceptions import UniqueDublicateError
from database.models import User


async def add_user(tg_id: int) -> None:
    """Asynchronously add a new user to the database.

    Args:
        tg_id (int): The Telegram ID of the user to be added.

    Raises:
        UniqueDublicateError: If a user with the same Telegram ID already exists in the database.
    """
    async with async_session_maker() as session:
        new_user = User(
            user_tg_id=tg_id,
        )
        try:
            session.add(new_user)
            await session.commit()
        except IntegrityError as exception:
            await session.rollback()  # noqa: ASYNC120
            if is_unique_error(exception):
                raise UniqueDublicateError("Failed to add user due to integrity error") from exception
        await session.refresh(new_user)


# name of this function is bool-like.
async def user_exist_by_id(session: AsyncSession, tg_id: int) -> bool:  # noqa: FNE005
    """Check if a user exists in the database by their Telegram ID.

    Args:
        session (AsyncSession): The SQLAlchemy async session to use for the query.
        tg_id (int): The Telegram ID of the user to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    select_result = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user = select_result.scalars().first()
    return bool(user)
