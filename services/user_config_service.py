"""Services for user configuration operations."""
from database.crud.user_config import get_user_config_by_id
from database.exceptions import UserConfigNotFoundError


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
    return user_config.currency  # type: ignore
