"""Module contains the registration handler for new users."""
from aiogram import F, Router, types  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from config import LANGUAGES
from handlers.basic.states import RegistrationStates, start_menu
from handlers.error_utils import handle_error_situation
from handlers.keyboard import get_menu_keyboard, get_registration_category_keyboard
from services.users_service import UserNotRegisteredError, add_user

registration_router: Router = Router()


async def start_registration(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Initiate the registration process.

    Args:
        message (types.Message): The message object containing information about the user and the message.
        state (FSMContext): The finite state machine context to manage the state of the user.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    if message.from_user is None:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_USER_INFO"), _ensure_safe_exit)
        return

    await state.set_state(RegistrationStates.waiting_for_language)

    await message.answer(
        i18n.get("GET_LANGAUGE_MESSAGE"),
        reply_markup=_get_language_inline_keyboard(),
    )


@registration_router.callback_query(F.data == "en", RegistrationStates.waiting_for_language)
@registration_router.callback_query(F.data == "ru", RegistrationStates.waiting_for_language)
async def set_language_handler(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the language selection callback for the user.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing the user's selection.
        state (FSMContext): The finite state machine context to manage the state of the user.
        i18n (I18nContext): The internationalization context to handle multilingual support.
    """
    if not callback_query.message or not callback_query.from_user:
        return

    language = callback_query.data
    if not language:
        return

    await state.update_data(locale=language)
    await state.set_state(RegistrationStates.waiting_for_currency)
    await callback_query.message.answer(
        i18n.get("GET_CURRENCY_MESSAGE"),
    )


@registration_router.message(RegistrationStates.waiting_for_currency)
async def currency_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the currency selection for the user.

    Args:
        message (types.Message): The message object containing user information and message details.
        state (FSMContext): The finite state machine context to manage the state of the user.
        i18n (I18nContext): The internationalization context to handle multilingual support.
    """
    if message.from_user is None:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_USER_INFO"), _ensure_safe_exit)
        return

    currency = message.text
    if not currency:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_CURRENCY"), _ensure_safe_exit)

    await state.update_data(currency=currency)
    await state.set_state(RegistrationStates.waiting_for_categories)
    await message.answer(
        i18n.get("GET_CATEGORIES_MESSAGE"),
        reply_markup=get_registration_category_keyboard(i18n),
    )


@registration_router.message(
    RegistrationStates.waiting_for_categories,
    F.text != LazyProxy("REGISTRATION_CATEGORY_END_BUTTON"),
)
async def categories_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the addition of new categories during the registration process.

    This asynchronous function processes a message from the user to add a new category
    to their list of categories. It performs the following steps:
    1. Checks if the message contains user information. If not, it handles the error.
    2. Retrieves the new category from the message text.
    3. If the new category is empty, it handles the error.
    4. Retrieves the current state data and appends the new category to the list of categories.
    5. Updates the state with the new list of categories.
    6. Sends a message to the user asking for the next category, with a keyboard for input.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context for managing user state.
        i18n (I18nContext): The internationalization context for handling translations.
    """
    if message.from_user is None:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_USER_INFO"), _ensure_safe_exit)
        return

    new_category = message.text
    if not new_category:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_CATEGORIES"), _ensure_safe_exit)
    state_data = await state.get_data()
    categories = state_data.get("categories", [])
    categories.append(new_category)
    await state.update_data(categories=categories)
    await message.answer(
        i18n.get("GET_NEXT_CATEGORY_MESSAGE"),
        reply_markup=get_registration_category_keyboard(i18n),
    )


@registration_router.message(F.text == LazyProxy("REGISTRATION_CATEGORY_END_BUTTON"))
async def end_registration_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the end of the registration process.

    This asynchronous function handles the end of the registration process by performing the following steps:
    1. Retrieves the user information from the message.
    2. Retrieves the current state data.
    3. If the user information is not present, it handles the error.
    4. If the state data is not present, it handles the error.
    5. Retrieves the user's language and currency from the state data.
    6. Retrieves the list of categories from the state data.
    7. Sends a message to the user with the registration details.
    8. Resets the state to the start menu.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context for managing user state.
        i18n (I18nContext): The internationalization context for handling translations.
    """
    if message.from_user is None:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_USER_INFO"), _ensure_safe_exit)
        return

    state_data = await state.get_data()
    if not state_data:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_REGISTRATION"), _ensure_safe_exit)
        return

    language = state_data.get("locale")
    currency = state_data.get("currency")
    categories = state_data.get("categories")

    if not language or not currency or not categories:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_REGISTRATION"), _ensure_safe_exit)
        return
    try:
        await add_user(
            message.from_user.id,
            language,
            currency,
            categories,
        )
    except UserNotRegisteredError:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_REGISTRATION"), _ensure_safe_exit)
        return

    registration_details = i18n.get(
        "REGISTRATION_SUCCESS",
        language=LANGUAGES[language],
        currency=currency,
        categories=", ".join(categories),
    )
    await message.answer(registration_details, reply_markup=get_menu_keyboard(i18n))
    await _ensure_safe_exit(state)


def _get_language_inline_keyboard() -> types.InlineKeyboardMarkup:
    """Create an inline keyboard markup for language selection.

    The keyboard contains two buttons for selecting languages:
    English ("en") and Russian ("ru").

    Returns:
        types.InlineKeyboardMarkup: An inline keyboard markup with language selection buttons.
    """
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=LANGUAGES["en"],
                    callback_data="en",
                ),
                types.InlineKeyboardButton(
                    text=LANGUAGES["ru"],
                    callback_data="ru",
                ),
            ],
        ],
    )


async def _ensure_safe_exit(state: FSMContext) -> None:
    """Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.
    """
    await state.set_state(start_menu)
    await state.update_data(
        currency=None,
        categories=[],
    )
