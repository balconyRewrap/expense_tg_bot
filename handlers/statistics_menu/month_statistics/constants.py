"""Module defines constants and navigation callback data used in the "month_statistics".

Constants:
- ALL_CATEGORIES_NAME: A string representing the name for selecting all categories.
- END_CATEGORIES_SELECT_CALLBACK_DATA: A string representing the callback data
    for ending the category selection process.

NavigationCallbackData Instances:
- STATISTICS_CATEGORIES_PAGES_NAVIGATION: Navigation callback data for navigating
    through pages of category expenses statistics.
- CATEGORIES_CHOOSE_PAGES_NAVIGATION: Navigation callback data for navigating
    through pages when choosing a category.
"""
from handlers.handlers_utils import NavigationCallbackData

ALL_CATEGORIES_NAME = "all_categories"

END_CATEGORIES_SELECT_CALLBACK_DATA = "end_categories_select"

STATISTICS_CATEGORIES_PAGES_NAVIGATION = NavigationCallbackData(
    next_page="next_page_category_expenses",
    prev_page="prev_page_category_expenses",
)

CATEGORIES_CHOOSE_PAGES_NAVIGATION = NavigationCallbackData(
    next_page="next_page_choose_category",
    prev_page="prev_page_choose_category",
)

STATISTICS_CATEGORIES_PAGES_NAVIGATION = NavigationCallbackData(
    next_page="next_page_category_expenses",
    prev_page="prev_page_category_expenses",
)
