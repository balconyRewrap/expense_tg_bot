"""Handler for month statistics menu in the bot."""
from aiogram import F, Router, types  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from handlers.error_utils import handle_error_situation
from handlers.handlers_utils import SelectedCategory, get_navigation_inline_keyboard
from handlers.keyboards import get_statistics_menu_keyboard
from handlers.statistics_menu import statistics_utils
from handlers.statistics_menu.month_statistics import constants
from handlers.statistics_menu.month_statistics.states import MonthStatisticsStatesGroup
from handlers.statistics_menu.states import statistics_menu
from services.expenses_service import ALL_CATEGORIES_ID, ExpensePeriod

month_statistics_router: Router = Router()


@month_statistics_router.message(statistics_menu, F.text == LazyProxy("SHOW_MONTH_EXPENSES_STATISTICS_BUTTON"))
async def month_statistcs_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the month statistics menu interaction for the user.

    This function is triggered when a user accesses the month statistics menu.
    It validates the user's information, sets the appropriate state for selecting
    categories, and sends a message prompting the user to choose expense categories
    for month statistics.

    Args:
        message (types.Message): The incoming Telegram message object.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized strings.
    """
    if message.from_user is None:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=statistics_utils.ensure_safe_exit,
        )
        return
    await state.set_state(MonthStatisticsStatesGroup.selecting_categories)
    await state.update_data(period=ExpensePeriod.MONTH)
    await message.answer(
        text=i18n.get("CHOOSE_EXPENSE_CUSTOM_STATISTICS_CATEGORIES"),
        reply_markup=await statistics_utils.get_categories_inline_keyboard_markup(
            tg_id=message.from_user.id,
            page=0,
            i18n=i18n,
            categories_choose_pages_navigation=constants.CATEGORIES_CHOOSE_PAGES_NAVIGATION,
            all_categories_name=constants.ALL_CATEGORIES_NAME,
            end_categories_select_callback_data=constants.END_CATEGORIES_SELECT_CALLBACK_DATA,
        ),
    )


@month_statistics_router.callback_query(
    F.data == "next_page_choose_category",
    MonthStatisticsStatesGroup.selecting_categories,
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

    await statistics_utils.handle_categories_list(
        user_id=user_id,
        message=callback_query.message,
        state=state,
        i18n=i18n,
        categories_choose_pages_navigation=constants.CATEGORIES_CHOOSE_PAGES_NAVIGATION,
        all_categories_name=constants.ALL_CATEGORIES_NAME,
        end_categories_select_callback_data=constants.END_CATEGORIES_SELECT_CALLBACK_DATA,
    )


@month_statistics_router.callback_query(
    F.data == "prev_page_choose_category",
    MonthStatisticsStatesGroup.selecting_categories,
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

    await statistics_utils.handle_categories_list(
        user_id=user_id,
        message=callback_query.message,
        state=state,
        i18n=i18n,
        categories_choose_pages_navigation=constants.CATEGORIES_CHOOSE_PAGES_NAVIGATION,
        all_categories_name=constants.ALL_CATEGORIES_NAME,
        end_categories_select_callback_data=constants.END_CATEGORIES_SELECT_CALLBACK_DATA,
    )


@month_statistics_router.callback_query(
    MonthStatisticsStatesGroup.selecting_categories,
    (F.data.not_contains("page") & F.data != constants.END_CATEGORIES_SELECT_CALLBACK_DATA),
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
            ensure_safe_exit=statistics_utils.ensure_safe_exit,
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
            ensure_safe_exit=statistics_utils.ensure_safe_exit,
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
        i18n.get("WAIT_FOR_MONTH_STATISTICS"),
        reply_markup=get_statistics_menu_keyboard(i18n),
    )
    await statistics_utils.send_statistics(
        user_id=callback_query.from_user.id,
        message=callback_query.message,
        state=state,
        i18n=i18n,
        statistics_navigation_callback_data=constants.STATISTICS_CATEGORIES_PAGES_NAVIGATION,
    )


@month_statistics_router.callback_query(
    MonthStatisticsStatesGroup.selecting_categories,
    (F.data.not_contains("page") & F.data == constants.END_CATEGORIES_SELECT_CALLBACK_DATA),
)
async def handle_end_category_select(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the end of category selection in the month statistics menu.

    This function processes the callback query when a user selects a category
    in the month statistics menu. It validates the callback query, ensures
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
            ensure_safe_exit=statistics_utils.ensure_safe_exit,
        )
        return
    await state.set_state(statistics_menu)
    await callback_query.message.answer(i18n.get("WAIT_FOR_MONTH_STATISTICS"))
    await statistics_utils.send_statistics(
        user_id=callback_query.from_user.id,
        message=callback_query.message,
        state=state,
        i18n=i18n,
        statistics_navigation_callback_data=constants.STATISTICS_CATEGORIES_PAGES_NAVIGATION,
    )


@month_statistics_router.callback_query(
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

    statististics_pages = await statistics_utils.get_statistics_pages(user_id, callback_query.message, state, i18n)
    if not statististics_pages:
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_NO_STATISTICS"),
            ensure_safe_exit=statistics_utils.ensure_safe_exit,
        )
        return
    await callback_query.message.edit_text(
        text=statististics_pages[current_page],
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                get_navigation_inline_keyboard(
                    page=current_page,
                    total_pages=len(statististics_pages),
                    navigation_callback_data=constants.STATISTICS_CATEGORIES_PAGES_NAVIGATION,
                ),
            ],
        ),
    )


@month_statistics_router.callback_query(
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
    statististics_pages = await statistics_utils.get_statistics_pages(user_id, callback_query.message, state, i18n)
    if not statististics_pages:
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_NO_STATISTICS"),
            ensure_safe_exit=statistics_utils.ensure_safe_exit,
        )
        return
    await callback_query.message.edit_text(
        text=statististics_pages[current_page],
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                get_navigation_inline_keyboard(
                    page=current_page,
                    total_pages=len(statististics_pages),
                    navigation_callback_data=constants.STATISTICS_CATEGORIES_PAGES_NAVIGATION,
                ),
            ],
        ),
    )
