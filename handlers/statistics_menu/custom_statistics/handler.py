"""Module contains the handlers for the custom statistics menu in the Telegram bot."""
from datetime import datetime

from aiogram import F, Router, types  # noqa: WPS347  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from handlers.error_utils import handle_error_situation
from handlers.handlers_utils import SelectedCategory, get_navigation_inline_keyboard
from handlers.keyboards import get_statistics_menu_keyboard
from handlers.statistics_menu.custom_statistics import utils
from handlers.statistics_menu.custom_statistics.constants import (
    CUSTOM_PERIODS,
    DEFAULT_PERIODS,
    END_CATEGORIES_SELECT_CALLBACK_DATA,
    STATISTICS_CATEGORIES_PAGES_NAVIGATION,
)
from handlers.statistics_menu.custom_statistics.states import CustomStatisticsStatesGroup
from handlers.statistics_menu.states import statistics_menu
from services.expenses_service import ALL_CATEGORIES_ID

custom_statistics_router: Router = Router()


@custom_statistics_router.message(statistics_menu, F.text == LazyProxy("SHOW_CUSTOM_EXPENSES_STATISTICS_BUTTON"))
async def custom_statistics_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the custom statistics menu interaction.

    This function is triggered when the user accesses the custom statistics menu.
    It validates the user's information, sets the appropriate state for the
    custom statistics workflow, and prompts the user to select a period for
    custom expense statistics.

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
            ensure_safe_exit=utils.ensure_safe_exit,
        )
        return
    await state.set_state(CustomStatisticsStatesGroup.waiting_for_period)

    await message.answer(
        text=i18n.get("CHOOSE_EXPENSE_CUSTOM_STATISTICS_PERIOD"),
        reply_markup=utils.get_period_inline_keyboard_markup(i18n),
    )


@custom_statistics_router.callback_query(
    CustomStatisticsStatesGroup.waiting_for_period,
    F.data.in_(DEFAULT_PERIODS.values()),
)
async def handle_default_period_selection(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
) -> None:
    """Handle the selection of a default period for custom statistics.

    This function processes the callback query when a user selects a default
    period for custom statistics. It updates the state with the selected period,
    transitions to the category selection state, and sends a message prompting
    the user to choose expense categories.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing
            the user's selection and related metadata.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized
            messages.
    """
    if not callback_query.message or not isinstance(callback_query.message, types.Message):
        return
    await state.update_data(period=callback_query.data)
    await state.set_state(CustomStatisticsStatesGroup.selecting_categories)
    await callback_query.message.answer(
        i18n.get("CHOOSE_EXPENSE_CUSTOM_STATISTICS_CATEGORIES"),
        reply_markup=await utils.get_categories_inline_keyboard_markup(
            tg_id=callback_query.from_user.id,
            page=0,
            i18n=i18n,
        ),
    )


@custom_statistics_router.callback_query(
    CustomStatisticsStatesGroup.waiting_for_period,
    F.data.in_(CUSTOM_PERIODS.values()),
)
async def handle_custom_period_selection(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
) -> None:
    """Handle the selection of a custom period for statistics.

    This function is triggered when the user selects the option to input a custom
    time period for statistics. It validates the callback query, sets the state
    to wait for the start date of the custom period, and prompts the user to
    input the start date.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing
            information about the user's interaction.
        state (FSMContext): The finite state machine context for managing the
            current state of the user.
        i18n (I18nContext): The internationalization context for retrieving
            localized messages.
    """
    if not callback_query.message or not isinstance(callback_query.message, types.Message):
        return
    await state.set_state(CustomStatisticsStatesGroup.waiting_for_custom_period_start)
    await callback_query.message.answer(i18n.get("INPUT_CUSTOM_PERIOD_START_DATE"))


@custom_statistics_router.message(CustomStatisticsStatesGroup.waiting_for_custom_period_start)
async def handle_custom_period_start_date(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the input of the custom period start date in a Telegram bot.

    This function processes the user's message to validate and store the start date
    for a custom statistics period. It ensures the input is valid and transitions
    the state to await the end date of the custom period.

    Args:
        message (types.Message): The Telegram message object containing the user's input.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    if not message.from_user:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=utils.ensure_safe_exit,
        )
        return
    if not message.text:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_DATE"),
        )
        return
    try:
        datetime.strptime(message.text, "%d.%m.%Y").date()  # noqa: DTZ007
    except ValueError:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_DATE_NOT_VALID"),
        )
        return

    await state.update_data(custom_period_start_date=message.text)
    await state.set_state(CustomStatisticsStatesGroup.waiting_for_custom_period_end)
    await message.answer(i18n.get("INPUT_CUSTOM_PERIOD_END_DATE"))


@custom_statistics_router.message(CustomStatisticsStatesGroup.waiting_for_custom_period_end)
async def handle_custom_period_end_date(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the input of the custom period end date in a Telegram bot conversation.

    This function validates the user's input for the end date of a custom period,
    updates the state with the provided date if valid, and transitions to the next
    state where the user selects categories for custom statistics.

    Args:
        message (types.Message): The Telegram message object containing the user's input.
        state (FSMContext): The finite state machine context for managing conversation states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    if not message.from_user:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=utils.ensure_safe_exit,
        )
        return
    if not message.text:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_DATE"),
        )
        return
    try:
        datetime.strptime(message.text, "%d.%m.%Y").date()  # noqa: DTZ007
    except ValueError:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_DATE_NOT_VALID"),
        )
        return

    await state.update_data(custom_period_end_date=message.text)
    await state.set_state(CustomStatisticsStatesGroup.selecting_categories)
    await message.answer(
        i18n.get("CHOOSE_EXPENSE_CUSTOM_STATISTICS_CATEGORIES"),
        reply_markup=await utils.get_categories_inline_keyboard_markup(
            tg_id=message.from_user.id,
            page=0,
            i18n=i18n,
        ),
    )


@custom_statistics_router.callback_query(
    F.data == "next_page_choose_category",
    CustomStatisticsStatesGroup.selecting_categories,
)
async def next_page_choose_category_button_handler(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
) -> None:
    """Handle the "next page" button press in the category selection menu.

    This function updates the current page index for the category selection menu
    in the user's state. If the user is already on the last page, it resets the
    page index to the first page. Otherwise, it increments the page index by one.
    After updating the state, it calls a helper function to handle the updated
    category list display.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing
            information about the button press event.
        state (FSMContext): The finite state machine context for managing user-specific
            state data.
        i18n (I18nContext): The internationalization context for handling localized
            messages.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    # it takes user_id from callback query, not message, because user_id from message is nonsense
    user_id = callback_query.from_user.id
    state_data = await state.get_data()
    current_page = state_data.get("current_page_choose_category", 0)
    last_page = state_data.get("last_page_choose_category", 0)
    if current_page == last_page:
        await state.update_data(current_page_choose_category=0)
    else:
        await state.update_data(current_page_choose_category=current_page + 1)

    await utils.handle_categories_list(user_id, callback_query.message, state, i18n)


@custom_statistics_router.callback_query(
    F.data == "prev_page_choose_category",
    CustomStatisticsStatesGroup.selecting_categories,
)
async def prev_page_choose_category_button_handler(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
) -> None:
    """Handle the "previous page" button press in the category selection menu.

    This function updates the current page in the state to the previous page
    or wraps around to the last page if the current page is the first one.
    It then calls a helper function to update the category list display.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing
            information about the button press event.
        state (FSMContext): The finite state machine context for managing user state.
        i18n (I18nContext): The internationalization context for handling translations.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    # it takes user_id from callback query, not message, because user_id from message is nonsense
    user_id = callback_query.from_user.id
    state_data = await state.get_data()
    current_page = state_data.get("current_page_choose_category", 0)
    last_page = state_data.get("last_page_choose_category", 0)

    if current_page == 0:
        await state.update_data(current_page_choose_category=last_page)
    else:
        await state.update_data(current_page_choose_category=current_page - 1)

    await utils.handle_categories_list(user_id, callback_query.message, state, i18n)


@custom_statistics_router.callback_query(
    CustomStatisticsStatesGroup.selecting_categories,
    (F.data.not_contains("page") & F.data != END_CATEGORIES_SELECT_CALLBACK_DATA),
)
async def handle_category(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the selection of a category in the statistics menu.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing data about the user's interaction.
        state (FSMContext): The finite state machine context for managing user state.
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
            ensure_safe_exit=utils.ensure_safe_exit,
        )
        return
    callback_data = SelectedCategory.unpack(callback_query.data)
    category_id = callback_data.category_id
    category_name = callback_data.category_name
    if not (category_name and category_id):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_UNKNOWN"),
            ensure_safe_exit=utils.ensure_safe_exit,
        )
        return
    state_data = await state.get_data()

    categories: dict[int, str] = state_data.get("categories", {})
    categories[category_id] = category_name
    await state.update_data(categories=categories)
    if category_id != ALL_CATEGORIES_ID:
        return
    await state.set_state(statistics_menu)
    await callback_query.message.answer(
        i18n.get("WAIT_FOR_CUSTOM_STATISTICS"),
        reply_markup=get_statistics_menu_keyboard(i18n),
    )
    await utils.send_statistics(callback_query.from_user.id, callback_query.message, state, i18n)


@custom_statistics_router.callback_query(
    CustomStatisticsStatesGroup.selecting_categories,
    (F.data.not_contains("page") & F.data == END_CATEGORIES_SELECT_CALLBACK_DATA),
)
async def handle_end_category_select(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the end of category selection in the custom statistics menu.

    This function processes the callback query when a user selects a category
    in the custom statistics menu. It validates the callback query, ensures
    the user's information is present, and transitions the state to the
    statistics menu. If an error occurs, it handles the situation gracefully
    by notifying the user and ensuring a safe exit.

    Args:
        callback_query (types.CallbackQuery): The callback query object
            containing information about the user's interaction.
        state (FSMContext): The finite state machine context for managing
            user states.
        i18n (I18nContext): The internationalization context for retrieving
            localized messages.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    if not (callback_query.data and callback_query.from_user and callback_query.message):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=utils.ensure_safe_exit,
        )
        return
    await state.set_state(statistics_menu)
    await callback_query.message.answer(i18n.get("WAIT_FOR_CUSTOM_STATISTICS"))
    await utils.send_statistics(callback_query.from_user.id, callback_query.message, state, i18n)


@custom_statistics_router.callback_query(
    F.data == "next_page_category_expenses",
    statistics_menu,
)
async def next_page_category_expenses_button_handler(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
) -> None:
    """Handle the navigation to the next page of category expenses in a statistics menu.

    This function is triggered when the user interacts with a button to navigate to the next page
    of category expenses. It updates the current page in the state, retrieves the statistics pages,
    and updates the message text with the content of the new page.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing information
            about the user's interaction with the inline button.
        state (FSMContext): The finite state machine context for storing and retrieving user-specific
            data during the bot's operation.
        i18n (I18nContext): The internationalization context for retrieving localized strings.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    # it takes user_id from callback query, not message, because user_id from message is nonsense
    user_id = callback_query.from_user.id
    state_data = await state.get_data()
    current_page = state_data.get("current_page_category_expenses", 0)
    last_page = state_data.get("last_page_category_expenses", 0)
    if current_page == last_page:
        current_page = 0
    else:
        current_page += 1
    await state.update_data(current_page_category_expenses=current_page)

    statististics_pages = await utils.get_statistics_pages(user_id, callback_query.message, state, i18n)
    if not statististics_pages:
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_NO_STATISTICS"),
            ensure_safe_exit=utils.ensure_safe_exit,
        )
        return
    await callback_query.message.edit_text(
        text=statististics_pages[current_page],
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                get_navigation_inline_keyboard(
                    page=current_page,
                    total_pages=len(statististics_pages),
                    navigation_callback_data=STATISTICS_CATEGORIES_PAGES_NAVIGATION,
                ),
            ],
        ),
    )


@custom_statistics_router.callback_query(
    F.data == "prev_page_category_expenses",
    statistics_menu,
)
async def prev_page_category_expenses_button_handler(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
) -> None:
    """Handle the "previous page" button for navigating category expenses statistics.

    This function is triggered when the user interacts with the "previous page" button
    in the category expenses statistics menu. It updates the current page in the state
    and displays the corresponding statistics page.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing information
            about the user's interaction with the button.
        state (FSMContext): The finite state machine context for managing user-specific data.
        i18n (I18nContext): The internationalization context for retrieving localized strings.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    # it takes user_id from callback query, not message, because user_id from message is nonsense
    user_id = callback_query.from_user.id
    state_data = await state.get_data()
    current_page = state_data.get("current_page_category_expenses", 0)
    last_page = state_data.get("last_page_category_expenses", 0)

    if current_page == 0:
        current_page = last_page
    else:
        current_page -= 1
    await state.update_data(current_page_category_expenses=current_page)
    statististics_pages = await utils.get_statistics_pages(user_id, callback_query.message, state, i18n)
    if not statististics_pages:
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_NO_STATISTICS"),
            ensure_safe_exit=utils.ensure_safe_exit,
        )
        return
    await callback_query.message.edit_text(
        text=statististics_pages[current_page],
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                get_navigation_inline_keyboard(
                    page=current_page,
                    total_pages=len(statististics_pages),
                    navigation_callback_data=STATISTICS_CATEGORIES_PAGES_NAVIGATION,
                ),
            ],
        ),
    )
