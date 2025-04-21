# -----------------------------
# ❌ ERROR MESSAGES
# -----------------------------

# BASE ERRORS
ERROR_USER_INFO = Error: Failed to retrieve user information.

ERROR_UNKNOWN = An unknown error occurred. Please try again.

COMMAND_NOT_RECOGNIZED = Command not recognized.  
    Please use /start or the buttons below.

# FINAL ERRORS
ERROR_REGISTRATION = Error: Failed to register user.

ERROR_EXPENSE_NOT_ADDED = 
    Error: Failed to add expense.

    Please try again.

ERROR_CATEGORY_NOT_ADDED =
    Error: Failed to add category.

    Please try again.

# NOT VALID ERROR
ERROR_AMOUNT_NOT_VALID = Unfortunately, the entered amount is not valid.  
     Please try again.

ERROR_NAME_NOT_VALID = 
    Unfortunately, the entered expense name is not valid.  
    Please try again.

ERROR_DATE_NOT_VALID = 
    Unfortunately, the entered date is not valid.  
    Please try again in DD.MM.YYYY format.

# NOT GOTTEN ERROR
ERROR_CURRENCY = Error: Failed to retrieve selected currency.

ERROR_CATEGORIES = Error: Failed to retrieve category.

ERROR_USER_CURRENCY = 
    Error: Failed to retrieve selected currency.

    Perhaps you haven’t selected a currency. Please choose one in the settings.

ERROR_DATE = Error: Failed to retrieve the date.

ERROR_NO_CATEGORIES_SELECTED = 
    Error: No categories selected.

    Please select one or more categories.

# INFO FROM DB ERROR
ERROR_NO_CATEGORIES = 
    Error: You don't have any categories.

    Please add categories in the settings.

ERROR_NO_CURRENCIES = No previous currencies found.

ERROR_NO_EXPENSES_PAGE_MESSAGE = 
    You have no expenses for the selected period in the category { $category_name }.

    Please add expenses.

ERROR_NO_STATISTICS = 
    You have no statistics for the selected period and categories.

    Please add expenses.

# -----------------------------
# 📝 PROMPT MESSAGES
# -----------------------------

# CHOOSE PROMPT MESSAGES
CHOOSE_LANGAUGE_MESSAGE = Choose a language from the list below.

CHOOSE_CATEGORY = Please choose a category from the list below.  
    If the category you need is not listed, go to settings and add it.

CHOOSE_SETTINGS_MENU_ITEM = Choose a settings menu item.  
    To return to the main menu, press the "Main Menu" button.

CHOOSE_CATEGORY_SETTINGS_MENU_ITEM = Choose a category settings menu item.  
    To return to settings, press the "Bot Settings" button.

CHOOSE_CATEGORY_TO_REMOVE = Choose the category you want to remove.  
    To return to settings, press the "Bot Settings" button.

CHOOSE_STATISTICS_METHOD = Choose an expense analysis method.  
    To return to the main menu, press the "Main Menu" button.

CHOOSE_EXPENSE_STATISTICS_PERIOD = 
    Choose the period for which you want to see the statistics.  
    To return to the main menu, press the "Main Menu" button.

CHOOSE_EXPENSE_CUSTOM_STATISTICS_CATEGORIES =
    Choose a category for which you want to see statistics.  
    When done selecting categories, press the corresponding button.  
    To return to the main menu, press the "Main Menu" button.

# INPUT PROMPT MESSAGES
INPUT_CURRENCY_MESSAGE = Enter the currency you want to use.  
    For example: RUB, USD, EUR  
    Previously used currencies:  
    { $currencies }  
    When you finish, press the button below.

INPUT_CATEGORIES_REGISTRATION_MESSAGE = Enter expense categories.  
    For example: Groceries, Transport, Clothing  
    When you finish, press the button below.  
    To change categories later, go to settings.

INPUT_CATEGORIES_MESSAGE = Enter expense categories.  
    For example: Groceries, Transport, Clothing  
    When you finish, press the button below.

INPUT_NEXT_CATEGORY_MESSAGE = Enter the next category.  
    To finish input, press the button below.

INPUT_AMOUNT_MESSAGE = Enter the amount spent in { $currency }.  
    To change the currency, go to settings.

INPUT_EXPENSE_NAME = Please enter a name for the expense.

INPUT_CUSTOM_PERIOD_START_DATE = Enter the start date of the period in DD.MM.YYYY format.  
    For example: 01.01.2021

INPUT_CUSTOM_PERIOD_END_DATE = Enter the end date of the period in DD.MM.YYYY format.  
    For example: 31.12.2021

# OTHER PROMPT MESSAGES
REGISTRATION_REQUIRED = Please register to start using the bot.  
    For using the bot, please register.

CONFIRM_EXPENSE = 
    Please confirm the entered data:  
    Name: { $name }  
    Category: { $category_name }  
    Amount: { $amount } { $currency }  
    If everything is correct, press "Add Expense", otherwise "Do Not Add Expense".

CONFIRM_REMOVE_CATEGORY =
    Please confirm the removal of the category:  
    Category: { $category_name }  
    If everything is correct, press "Remove Category", otherwise "Do Not Remove Category".

CONFIRM_CURRENCY_CHANGE = 
    Please confirm the currency change:  
    Currency: { $currency }  
    If everything is correct, press "Change Currency", otherwise "Do Not Change Currency".

# -----------------------------
# ✅ SUCCESS MESSAGES
# -----------------------------

EXPENSE_ADDED = Expense successfully added!

CATEGORY_REMOVED = Category successfully removed!

REGISTRATION_SUCCESS = 
    You have successfully registered!  
    Selected language: { $language }  
    Selected currency: { $currency }  
    Expense categories: { $categories }

CATEGORIES_ADDED_MESSAGE = Categories successfully added!

CURRENCY_CHANGED = Currency successfully changed!

LANGUAGE_CHANGED = Language successfully changed!

# -----------------------------
# ⏳ WAITING MESSAGES
# -----------------------------
WAIT_FOR_CUSTOM_STATISTICS = Please wait, calculating custom statistics...

WAIT_FOR_MONTH_STATISTICS = Please wait, calculating monthly statistics...

# -----------------------------
# ℹ️ OTHER TEXTS
# -----------------------------

START_MESSAGE = Welcome to the expense tracking bot!

CANCELLED_EXPENSE = Expense cancelled.

CANCELLED_REMOVE_CATEGORY = Category removal cancelled.

CANCELLED_CHANGE_CURRENCY = Currency change cancelled.

CUSTOM_STATISTICS_PAGE = Statistics for selected parameters:  
    Category: { $category_name }  
    Total spent during the period:  
    { $total_expenses }

CUSTOM_STATISTICS_CURRENCY_SUM = 
    - { $amount } { $currency }

# -----------------------------
# 🎛️ BUTTONS
# -----------------------------

# CANCEL/END BUTTON
MAIN_MENU_BUTTON = Main Menu
CATEGORY_END_BUTTON = Finish Category Input

# MAIN MENU BUTTONS
ADD_EXPENSE_BUTTON = Add Expense
SHOW_EXPENSES_BUTTON = Expense Analysis
SETTINGS_MENU_BUTTON = Bot Settings

# ADD EXPENSE BUTTONS
CONFIRM_EXPENSE_BUTTON = Add Expense
CANCEL_EXPENSE_BUTTON = Do Not Add Expense

# SETTINGS MENU BUTTONS
CATEGORIES_SETTINGS_MENU_BUTTON = Category Settings
CHANGE_CURRENCY_MENU_BUTTON = Change Currency
CHANGE_LANGUAGE_MENU_BUTTON = Change Language

# CATEGORY SETTINGS MENU BUTTONS
ADD_CATEGORY_BUTTON = Add Category/ies
REMOVE_CATEGORY_BUTTON = Remove Category/ies

# REMOVE CATEGORY BUTTONS
CONFIRM_REMOVE_CATEGORY_BUTTON = Remove Category
CANCEL_REMOVE_CATEGORY_BUTTON = Do Not Remove Category

# CHANGE CURRENCY BUTTONS
CONFIRM_CHANGE_CURRENCY_BUTTON = Change Currency
CANCEL_CHANGE_CURRENCY_BUTTON = Do Not Change Currency

# STATISTICS MENU BUTTONS
SHOW_CUSTOM_EXPENSES_STATISTICS_BUTTON = Show Category and Date Statistics
SHOW_MONTH_EXPENSES_STATISTICS_BUTTON = Show Monthly Statistics

# CUSTOM STATISTICS BUTTONS
DAY_PERIOD_BUTTON = For a Day
WEEK_PERIOD_BUTTON = For a Week
MONTH_PERIOD_BUTTON = For a Month
YEAR_PERIOD_BUTTON = For a Year
ALL_PERIOD_BUTTON = All Time
CUSTOM_PERIOD_BUTTON = Custom Period

ALL_CATEGORIES_BUTTON = All Categories
END_CATEGORIES_SELECT_BUTTON = Finish Category Selection
