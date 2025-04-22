"""Module defines constants and callback data used in the custom statistics handler of the expense tracking bot.

Attributes:
    DEFAULT_PERIODS (Final[dict]): A dictionary mapping button identifiers to their corresponding period strings.

        - "DAY_PERIOD_BUTTON": Represents the daily period.
        - "WEEK_PERIOD_BUTTON": Represents the weekly period.
        - "MONTH_PERIOD_BUTTON": Represents the monthly period.
        - "YEAR_PERIOD_BUTTON": Represents the yearly period.
        - "ALL_PERIOD_BUTTON": Represents the all-time period.

    CUSTOM_PERIODS (Final[dict]): A dictionary mapping button identifiers to their corresponding custom period strings.

        - "CUSTOM_PERIOD_BUTTON": Represents a custom period.

    CATEGORIES_CHOOSE_PAGES_NAVIGATION (NavigationCallbackData): Callback data for navigating between pages.

        - next_page: Identifier for the next page.
        - prev_page: Identifier for the previous page.

    STATISTICS_CATEGORIES_PAGES_NAVIGATION (NavigationCallbackData): Callback data for navigating between pages.

        - next_page: Identifier for the next page.
        - prev_page: Identifier for the previous page.

    ALL_CATEGORIES_NAME (str): A string representing the name for all categories.

    END_CATEGORIES_SELECT_CALLBACK_DATA (str): A string representing the callback data for ending category selection.
"""
from typing import Final

from handlers.handlers_utils import NavigationCallbackData

# I've already make it final
DEFAULT_PERIODS: Final = {  # noqa: WPS407
    "DAY_PERIOD_BUTTON": "day_period",
    "WEEK_PERIOD_BUTTON": "week_period",
    "MONTH_PERIOD_BUTTON": "month_period",
    "YEAR_PERIOD_BUTTON": "year_period",
    "ALL_PERIOD_BUTTON": "all_time_period",
}

# I've already make it final
CUSTOM_PERIODS: Final = {  # noqa: WPS407
    "CUSTOM_PERIOD_BUTTON": "custom_period",
}

CATEGORIES_CHOOSE_PAGES_NAVIGATION = NavigationCallbackData(
    next_page="next_page_choose_category",
    prev_page="prev_page_choose_category",
)

STATISTICS_CATEGORIES_PAGES_NAVIGATION = NavigationCallbackData(
    next_page="next_page_category_expenses",
    prev_page="prev_page_category_expenses",
)

ALL_CATEGORIES_NAME = "all_categories"

END_CATEGORIES_SELECT_CALLBACK_DATA = "end_categories_select"
