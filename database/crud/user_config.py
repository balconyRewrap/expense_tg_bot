from sqlalchemy.sql import select

from database.config import async_session_maker
from database.exceptions import UserConfigNotFoundError
from database.models import UserConfig


async def get_user_config_by_id(id: int) -> UserConfig:
    """Retrieve the user configuration by user Telegram ID.

    Args:
        id (int): The Telegram ID of the user.

    Returns:
        UserConfig: The configuration settings of the user.

    Raises:
        UserConfigNotFoundError: If no configuration is found for the given user ID.
    """
    async with async_session_maker() as session:
        select_result = await session.execute(select(UserConfig).filter_by(user_tg_id=id))
        user_config = select_result.scalar.first()
        if not user_config:
            raise UserConfigNotFoundError(f"UserConfig for User with id {id} not found")
        return user_config
