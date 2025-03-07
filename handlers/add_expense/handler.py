from aiogram import F, Router, types  # noqa: WPS347
from aiogram.fsm.context import FSMContext

from handlers.add_expense.states import AddExpenseStatesGroup
from handlers.basic.keyboard import get_menu_keyboard, get_post_menu_keyboard
from handlers.basic.states import start_menu
from handlers.error_utils import handle_error_situation
from handlers.texts import (
    ADD_EXPENSE_BUTTON,
    ERROR_AMOUNT_NOT_VALID,
    ERROR_USER_CURRENCY,
    ERROR_USER_INFO,
    GET_AMOUNT_MESSAGE,
    GET_EXPENSE_NAME,
    ERROR_NAME_NOT_VALID,
    CHOOSE_CATEGORY,
)
from services.user_config_service import get_currency_by_tg_id

add_expense_router: Router = Router()
MAXIMUM_EXPENSE_AMOUNT = 1000000

@add_expense_router.message(start_menu, F.text.casefold() == ADD_EXPENSE_BUTTON.lower())
async def handle_add_expense(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        await handle_error_situation(message, state, ERROR_USER_INFO, _ensure_safe_exit)
        return

    user_tg_id = message.from_user.id
    await state.clear()
    currency = get_currency_by_tg_id(user_tg_id)
    if not currency:
        await handle_error_situation(message, state, ERROR_USER_CURRENCY, _ensure_safe_exit)
        return
    await message.answer(
        GET_AMOUNT_MESSAGE.format(currency=currency),
        reply_markup=get_post_menu_keyboard(),
    )
    await state.set_state(AddExpenseStatesGroup.entering_amount)


@add_expense_router.message(AddExpenseStatesGroup.entering_amount)
async def handle_amount(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        await handle_error_situation(message, state, ERROR_USER_INFO, _ensure_safe_exit)
        return

    if not message.text:
        await handle_error_situation(message, state, ERROR_AMOUNT_NOT_VALID, _ensure_safe_exit)
        return
    amount = _parse_amount(message.text)
    if amount is None:
        await handle_error_situation(message, state, ERROR_AMOUNT_NOT_VALID, _ensure_safe_exit)
        return
    await state.update_data(amount=amount)
    await state.set_state(AddExpenseStatesGroup.entering_name)
    await message.answer(GET_EXPENSE_NAME, reply_markup=get_post_menu_keyboard())


@add_expense_router.message(AddExpenseStatesGroup.entering_name)
async def handle_name(message: types.Message, state: FSMContext) -> None:
    if not message.text:
        await handle_error_situation(message, state, ERROR_NAME_NOT_VALID, _ensure_safe_exit)
        return
    await state.update_data(name=message.text)
    await state.set_state(AddExpenseStatesGroup.choosing_category)
    await message.answer(CHOOSE_CATEGORY, reply_markup=get_post_menu_keyboard())


def _parse_amount(text: str) -> int | None:
    try:
        amount = int(text)
        if 0 < amount <= MAXIMUM_EXPENSE_AMOUNT:
            return amount
    except ValueError:
        return None


async def _ensure_safe_exit(state: FSMContext) -> None:
    """
    Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.

    Returns:
        None
    """
    await state.set_state(start_menu)
    await state.update_data(
        amount=None,
        name=None,
    )