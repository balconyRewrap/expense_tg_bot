"""Handlers for changing the currency in the settings menu."""
from aiogram import F, Router, types  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from handlers.error_utils import handle_error_situation
from handlers.handlers_utils import get_confirmation_inline_keyboard_markup
from handlers.keyboards import get_post_menu_keyboard, get_settings_menu_keyboard
from handlers.settings_menu.change_currency.states import ChangeCurrencyStatesGroup
from handlers.settings_menu.states import settings_menu
from services.expenses_service import get_all_currencies_used_by_tg_id
from services.user_configs_service import UserConfigNotChangedError, set_currency_by_tg_id

change_currency_router: Router = Router()


@change_currency_router.message(settings_menu, F.text == LazyProxy("CHANGE_CURRENCY_MENU_BUTTON"))
async def change_currency_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the process of changing the currency in the settings menu.

    This asynchronous handler is triggered when a user initiates the currency change process.
    It validates the presence of user information, sets the appropriate state for awaiting
    currency input, and sends a message prompting the user to input the desired currency.

    Args:
        message (types.Message): The incoming message object from the user.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    if message.from_user is None:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await state.set_state(ChangeCurrencyStatesGroup.waiting_for_currency)
    currencies = await get_all_currencies_used_by_tg_id(message.from_user.id)
    currencies_text = "\n".join(currencies) if currencies else i18n.get("ERROR_NO_CURRENCIES")

    await message.answer(
        text=i18n.get("INPUT_CURRENCY_MESSAGE", currencies=currencies_text),
        reply_markup=get_post_menu_keyboard(i18n),
    )


@change_currency_router.message(ChangeCurrencyStatesGroup.waiting_for_currency)
async def set_currency_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the process of setting a new currency for the user.

    This asynchronous handler function is triggered when a user sends a message
    to set their preferred currency. It validates the user's input, updates the
    state with the new currency, and prompts the user to confirm the change.

    Args:
        message (types.Message): The incoming message object from the user.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized strings.
    """
    if message.from_user is None:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return

    currency = message.text
    if not currency:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_CURRENCY"), _ensure_safe_exit)
        return

    await state.update_data(currency=currency)
    await state.set_state(ChangeCurrencyStatesGroup.confirming_currency_change)
    await message.answer(
        i18n.get("CONFIRM_CURRENCY_CHANGE", currency=currency),
        reply_markup=get_confirmation_inline_keyboard_markup(
            i18n=i18n,
            confirm_i18n_text="CONFIRM_CHANGE_CURRENCY_BUTTON",
            cancel_i18n_text="CANCEL_CHANGE_CURRENCY_BUTTON",
        ),
    )


@change_currency_router.callback_query(ChangeCurrencyStatesGroup.confirming_currency_change, F.data == "confirm")
@change_currency_router.callback_query(ChangeCurrencyStatesGroup.confirming_currency_change, F.data == "cancel")
async def handle_confirmation(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the confirmation callback query in the settings menu for changing currency.

    This function processes the user's confirmation or cancellation input when interacting
    with the currency change confirmation menu. It ensures that the callback query contains
    valid data and user information, and handles errors or specific actions (e.g., cancel or confirm).

    Args:
        callback_query (types.CallbackQuery): The callback query object containing user interaction data.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    if not (callback_query.data and callback_query.from_user):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    if callback_query.data == "cancel":
        await _handle_cancel(callback_query, state, i18n)
        return
    await _handle_confirm(callback_query, state, i18n)


async def _handle_cancel(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the cancellation of the currency change process.

    This function ensures a safe exit from the current state and sends a cancellation
    message to the user. It also provides the settings menu keyboard for further actions.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing
            information about the user's interaction.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    await _ensure_safe_exit(state)
    if not callback_query.message:
        return
    await callback_query.message.answer(
        i18n.get("CANCELLED_CHANGE_CURRENCY"),
        reply_markup=get_settings_menu_keyboard(i18n),
    )


async def _handle_confirm(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the confirmation of a currency change in the settings menu.

    Args:
        callback_query (types.CallbackQuery): The callback query object triggered by the user interaction.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    if not callback_query.message or not isinstance(callback_query.message, types.Message):
        return
    state_data = await state.get_data()
    user_tg_id = callback_query.from_user.id
    currency = state_data.get("currency")
    if not all([user_tg_id, currency]):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_UNKNOWN"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await _ensure_safe_exit(state)
    try:
        # pyright do not understand not all() operation
        await set_currency_by_tg_id(user_tg_id, currency)  # pyright: ignore[reportArgumentType]
    except UserConfigNotChangedError:
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_UNKNOWN"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await callback_query.message.answer(i18n.get("CURRENCY_CHANGED"), reply_markup=get_settings_menu_keyboard(i18n))


async def _ensure_safe_exit(state: FSMContext) -> None:
    """Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.
    """
    await state.update_data(currency=None)
    await state.set_state(settings_menu)
