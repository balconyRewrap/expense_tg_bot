"""Module contains the LocaleManager class for managing the locale (language) settings for users."""
from aiogram.fsm.context import FSMContext
from aiogram.types.user import User
from aiogram_i18n.managers import FSMManager

from services.user_configs_service import get_language_by_tg_id, set_language_by_tg_id


class LocaleManager(FSMManager):
    """LocaleManager is responsible for managing the locale (language) settings for users."""

    async def get_locale(self, event_from_user: User, state: FSMContext) -> str:  # noqa: WPS615
        """Retrieve the locale for a user based on their state or Telegram ID.

        This method first attempts to get the locale from the provided state. If no locale is found in the state,
        it then attempts to retrieve the locale using the user's Telegram ID. If no locale is found through either
        method, a default locale of "ru" (Russian) is returned. If a locale is found using the Telegram ID, it is
        updated in the state.

        Args:
            event_from_user (User): The user object containing the Telegram user information.
            state (FSMContext): The finite state machine context for the user.

        Returns:
            str: The locale string for the user.
        """
        default = "ru"
        locale = await self._get_locale_from_state(state)
        if locale:
            return locale
        locale = await get_language_by_tg_id(event_from_user.id)
        if not locale:
            return default
        await state.update_data(locale=locale)
        return locale

    async def set_locale(self, locale: str, event_from_user: User, state: FSMContext) -> None:  # noqa: PLR6301, WPS615
        """Asynchronously sets the locale for a user and updates the state.

        Args:
            locale (str): The locale string to set for the user.
            event_from_user (User): The user event object containing user information.
            state (FSMContext): The finite state machine context to update with the new locale.
        """
        await state.update_data(locale=locale)
        await set_language_by_tg_id(event_from_user.id, locale)

    async def _get_locale_from_state(self, state: FSMContext) -> str | None:  # noqa: PLR6301
        """Retrieve the locale from the given FSMContext state.

        Args:
            state (FSMContext): The finite state machine context from which to retrieve the locale.

        Returns:
            str | None: The locale string if it exists in the state data, otherwise None.
        """
        state_data = await state.get_data()
        return state_data.get("locale")
