"""Module contains the handler functions for adding an expense in the expense tracking bot."""
from aiogram import F, Router, types  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.add_expense.states import AddExpenseStatesGroup
from handlers.basic.states import start_menu
from handlers.error_utils import handle_error_situation
from handlers.handlers_utils import (
    NavigationCallbackData,
    SelectedCategory,
    get_categories_inline_keyboard_and_total_pages,
)
from handlers.keyboards import get_menu_keyboard, get_post_menu_keyboard
from services.expenses_service import ExpenseNotAddedError, add_expense
from services.user_configs_service import get_currency_by_tg_id

add_expense_router: Router = Router()
MAXIMUM_EXPENSE_AMOUNT = 1000000

ADD_EXPENSE_CALLBACK_CATEGORY_DATA = NavigationCallbackData(
    next_page="next_page",
    prev_page="prev_page",
)


@add_expense_router.message(start_menu, F.text == LazyProxy("ADD_EXPENSE_BUTTON"))
async def handle_add_expense(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the addition of an expense by the user.

    This function is triggered when a user sends a message to add an expense. It performs the following steps:
    1. Checks if the user information is available in the message.
    2. Retrieves the user's currency based on their Telegram ID.
    3. Updates the state with the user's currency.
    4. Prompts the user to enter the amount for the expense.

    Args:
        message (types.Message): The message object containing the user's request to add an expense.
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

    user_tg_id = message.from_user.id
    currency = await get_currency_by_tg_id(user_tg_id)
    if not currency:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_CURRENCY"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await state.update_data(currency=currency)
    await message.answer(
        i18n.get("INPUT_AMOUNT_MESSAGE", currency=currency),
        reply_markup=get_post_menu_keyboard(i18n),
    )
    await state.set_state(AddExpenseStatesGroup.entering_amount)


@add_expense_router.message(AddExpenseStatesGroup.entering_amount)
async def handle_amount(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the amount input from the user.

    This function processes the amount entered by the user, validates it, and updates the state accordingly.
    If the user information is missing or the amount is invalid, it handles the error situation.

    Args:
        message (types.Message): The message object containing the user's input.
        state (FSMContext): The finite state machine context for the current user.
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

    if not message.text:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_AMOUNT_NOT_VALID"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    amount = _parse_amount(message.text)
    if amount is None:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_AMOUNT_NOT_VALID"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await state.update_data(amount=amount)
    await state.set_state(AddExpenseStatesGroup.entering_name)
    await message.answer(i18n.get("INPUT_EXPENSE_NAME"), reply_markup=get_post_menu_keyboard(i18n))


@add_expense_router.message(AddExpenseStatesGroup.entering_name)
async def handle_name(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the user's input for the expense name.

    This function processes the user's message to extract the expense name and updates the state accordingly.
    If the message does not contain text or user information, it handles the error situation.

    Args:
        message (types.Message): The message object containing the user's input.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized strings.
    """
    if not (message.text and message.from_user):
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await state.update_data(name=message.text)
    await state.set_state(AddExpenseStatesGroup.selecting_category)
    inline_keyboard_markup, total_pages = await get_categories_inline_keyboard_and_total_pages(
        message.from_user.id,
        page=0,
        navigation_callback_data=ADD_EXPENSE_CALLBACK_CATEGORY_DATA,
    )
    if not inline_keyboard_markup or not total_pages:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_NO_CATEGORIES"),
            ensure_safe_exit=_ensure_safe_exit,
        )
    # its already checked upper. Not 1 or Not None = True
    await state.update_data(current_page_category=0, last_page_category=total_pages - 1)  # pyright: ignore[reportOptionalOperand]
    await message.answer(
        i18n.get("CHOOSE_CATEGORY"),
        reply_markup=inline_keyboard_markup,
    )


@add_expense_router.callback_query(F.data == "next_page", AddExpenseStatesGroup.selecting_category)
async def next_page_button_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Handle the callback query for the "next page" button in the expense tracking bot.

    This function updates the current page of categories in the user's state and
    calls the function to handle displaying the categories list.

    Args:
        callback_query (types.CallbackQuery): The callback query object from the Telegram bot.
        state (FSMContext): The finite state machine context for the current user.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    # it takes user_id from callback query, not message, because user_id from message is nonsense
    user_id = callback_query.from_user.id
    state_data = await state.get_data()
    current_page = state_data.get("current_page_category", 0)
    last_page = state_data.get("last_page_category", 0)
    if current_page == last_page:
        await state.update_data(current_page_category=0)
    else:
        await state.update_data(current_page_category=current_page + 1)

    await _handle_categories_list(user_id, callback_query.message, state)


@add_expense_router.callback_query(F.data == "prev_page", AddExpenseStatesGroup.selecting_category)
async def prev_page_button_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Handle the callback query for the "previous page" button in the expense tracking bot.

    This function updates the current page of the category list to the previous page.
    If the current page is the first page, it wraps around to the last page.

    Args:
        callback_query (types.CallbackQuery): The callback query object from the Telegram bot.
        state (FSMContext): The finite state machine context for the current user.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    # it takes user_id from callback query, not message, because user_id from message is nonsense
    user_id = callback_query.from_user.id
    state_data = await state.get_data()
    current_page = state_data.get("current_page_category", 0)
    last_page = state_data.get("last_page_category", 0)

    if current_page == 0:
        await state.update_data(current_page_category=last_page)
    else:
        await state.update_data(current_page_category=current_page - 1)

    await _handle_categories_list(user_id, callback_query.message, state)


@add_expense_router.callback_query(AddExpenseStatesGroup.selecting_category, F.data.not_contains("page"))
async def handle_category(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the selection of an expense category from a callback query.

    Args:
        callback_query (types.CallbackQuery): The callback query containing the selected category data.
        state (FSMContext): The current state of the finite state machine.
        i18n (I18nContext): The internationalization context for retrieving localized strings.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    if not (callback_query.data and callback_query.from_user and callback_query.message):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    callback_data = SelectedCategory.unpack(callback_query.data)
    category_id = callback_data.category_id
    category_name = callback_data.category_name
    state_data = await state.get_data()
    expense_name = state_data.get("name")
    amount = state_data.get("amount")
    currency = state_data.get("currency")
    if not (expense_name and amount):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_UNKNOWN"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await state.update_data(category_id=category_id)
    await state.set_state(AddExpenseStatesGroup.confirming_expense)
    await callback_query.message.answer(
        i18n.get("CONFIRM_EXPENSE", name=expense_name, amount=amount, category_name=category_name, currency=currency),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i18n.get("CONFIRM_EXPENSE_BUTTON"),
                        callback_data="confirm",
                    ),
                    InlineKeyboardButton(
                        text=i18n.get("CANCEL_EXPENSE_BUTTON"),
                        callback_data="cancel",
                    ),
                ],
            ],
        ),
    )


@add_expense_router.callback_query(AddExpenseStatesGroup.confirming_expense, F.data == "confirm")
@add_expense_router.callback_query(AddExpenseStatesGroup.confirming_expense, F.data == "cancel")
async def handle_confirmation(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the confirmation callback query for adding an expense.

    This function processes the user's confirmation response for adding an expense.
    It validates the callback query data, retrieves necessary state data, and attempts
    to add the expense to the database. If any validation or operation fails, it handles
    the error appropriately by sending an error message to the user and ensuring a safe
    exit from the current state.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing the user's response.
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


async def _handle_categories_list(user_id: int, message: types.Message, state: FSMContext) -> None:
    if not message.from_user:
        return
    state_data = await state.get_data()
    current_page = state_data.get("current_page_category") or 0
    inline_keyboard_markup, _ = await get_categories_inline_keyboard_and_total_pages(
        user_id,
        page=current_page,
        navigation_callback_data=ADD_EXPENSE_CALLBACK_CATEGORY_DATA,
    )
    if not inline_keyboard_markup:
        return
    await message.edit_reply_markup(
        reply_markup=inline_keyboard_markup,
    )


async def _handle_cancel(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the cancellation of an expense operation.

    This function ensures a safe exit from the current state and sends a cancellation
    message to the user if a message is present in the callback query.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing the user's interaction data.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    await _ensure_safe_exit(state)
    if not callback_query.message:
        return
    await callback_query.message.answer(i18n.get("CANCELLED_EXPENSE"), reply_markup=get_menu_keyboard(i18n))


async def _handle_confirm(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the confirmation of adding an expense.

    This function is triggered by a callback query and processes the confirmation
    of adding an expense. It retrieves necessary data from the state, validates it,
    and attempts to add the expense. If any required data is missing or an error
    occurs during the addition of the expense, it handles the error appropriately.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing
            the user's interaction data.
        state (FSMContext): The finite state machine context for managing user state.
        i18n (I18nContext): The internationalization context for retrieving localized
            messages.
    """
    if not callback_query.message or not isinstance(callback_query.message, types.Message):
        return
    state_data = await state.get_data()
    user_tg_id = callback_query.from_user.id
    category_id = state_data.get("category_id")
    amount = state_data.get("amount")
    name = state_data.get("name")
    currency = state_data.get("currency")
    if not all([user_tg_id, category_id, amount, name, currency]):
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
        await add_expense(
            name=name,  # pyright: ignore[reportArgumentType]
            currency=currency,  # pyright: ignore[reportArgumentType]
            amount=amount,  # pyright: ignore[reportArgumentType]
            user_tg_id=user_tg_id,
            category_id=category_id,  # pyright: ignore[reportArgumentType]
        )
    except ExpenseNotAddedError:
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_EXPENSE_NOT_ADDED"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await callback_query.message.answer(i18n.get("EXPENSE_ADDED"), reply_markup=get_menu_keyboard(i18n))


def _parse_amount(text: str) -> float | None:
    """Parse the given text to extract an integer amount.

    Args:
        text (str): The text to be parsed.

    Returns:
        (float | None): The parsed amount if it is a valid float within the allowed range,
                    otherwise None.
    """
    try:
        amount = float(text)
        if 0 < amount <= MAXIMUM_EXPENSE_AMOUNT:
            return amount
    except ValueError:
        return None


async def _ensure_safe_exit(state: FSMContext) -> None:
    """Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.
    """
    await state.set_state(start_menu)
    await state.update_data(
        amount=None,
        name=None,
        category_id=None,
        currency=None,
        current_page_category=0,
        last_page_category=0,
    )
