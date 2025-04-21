# -----------------------------
# ❌ ERROR MESSAGES
# -----------------------------

# BASE ERRORS
ERROR_USER_INFO = Ошибка: не удалось получить информацию о пользователе.

ERROR_UNKNOWN = Произошла неизвестная ошибка. Пожалуйста, попробуйте еще раз.

COMMAND_NOT_RECOGNIZED = Команда не распознана.
    Пожалуйста, используйте /start или кнопки ниже.

# FINAL ERRORS
ERROR_REGISTRATION = Ошибка: не удалось зарегистрировать пользователя.

ERROR_EXPENSE_NOT_ADDED = 
    Ошибка: не удалось добавить трату.

    Пожалуйста, попробуйте еще раз.

ERROR_CATEGORY_NOT_ADDED =
    Ошибка: не удалось добавить категорию.

    Пожалуйста, попробуйте еще раз.

# NOT VALID ERROR
ERROR_AMOUNT_NOT_VALID = К сожалению, введенное количество затраченных средств
     не является валидным. Пожалуйста, повторите попытку

ERROR_NAME_NOT_VALID = 
    К сожалению, введенное название траты не является валидным.
    Пожалуйста, повторите попытку.

ERROR_DATE_NOT_VALID = 
    К сожалению, введенная дата не является валидной.
    Пожалуйста, повторите попытку в формате ДД.ММ.ГГГГ.

# NOT GOTTEN ERROR
ERROR_CURRENCY = Ошибка: не удалось получить выбранную валюту.

ERROR_CATEGORIES = Ошибка: не удалось получить категорию.

ERROR_USER_CURRENCY = 
    Ошибка: не удалось получить выбранную валюту.

    Возможно у вас не выбрана валюта, выберите, пожалуйста в настройках.

ERROR_DATE = Ошибка: не удалось получить дату.

ERROR_NO_CATEGORIES_SELECTED = 
    Ошибка: у вас нет выбранных категорий.

    Пожалуйста, выберите категорию/и.

# INFO FROM DB ERROR
ERROR_NO_CATEGORIES = 
    Ошибка: у вас нет категорий.

    Пожалуйста, добавьте категории в настройках.

ERROR_NO_CURRENCIES = Предыдущие валюты отсутствуют.

ERROR_NO_EXPENSES_PAGE_MESSAGE = 
    У вас нет трат за выбранный период в категории { $category_name }.

    Пожалуйста, добавьте траты.

ERROR_NO_STATISTICS = 
    У вас нет статистики за выбранный период по выбранным категориям.

    Пожалуйста, добавьте траты.

# -----------------------------
# 📝 PROMPT MESSAGES
# -----------------------------

# CHOOSE PROMPT MESSAGES
CHOOSE_LANGAUGE_MESSAGE = Выберите язык из списка ниже.

    Choose a language from the list below.

CHOOSE_CATEGORY = Выберите, пожалуйста, категорию из списка ниже.

    Если нужной категории нет, то перейдите в настройки и добавьте ее.


CHOOSE_SETTINGS_MENU_ITEM = Выберите пункт меню настроек.

    Если хотите вернуться в главное меню, нажмите кнопку "Главное меню".

CHOOSE_CATEGORY_SETTINGS_MENU_ITEM = Выберите пункт меню настроек категорий.

    Если хотите вернуться в настройки, нажмите кнопку "Настройки бота".

CHOOSE_CATEGORY_TO_REMOVE = Выберите категорию, которую хотите удалить.

    Если хотите вернуться в настройки, нажмите кнопку "Настройки бота".

CHOOSE_STATISTICS_METHOD = Выберите метод анализа трат.

    Если хотите вернуться в главное меню, нажмите кнопку "Главное меню".

CHOOSE_EXPENSE_STATISTICS_PERIOD = 
    Выберите период, за который хотите увидеть статистику.

    Если хотите вернуться в главное меню, нажмите кнопку "Главное меню".

CHOOSE_EXPENSE_CUSTOM_STATISTICS_CATEGORIES =
    Выберите категорию, по которой хотите увидеть статистику.

    Если хотите закончить выбор категорий, нажмите соответсвующую кнопку.

    Если хотите вернуться в главное меню, нажмите кнопку "Главное меню".


# INPUT PROMPT MESSAGES
INPUT_CURRENCY_MESSAGE = Введите валюту, которую хотите использовать.

    Например: RUB, USD, EUR

    Валюты использованные вами прежде:
    { $currencies }

    Как закончите заполнять, нажмите кнопку ниже.

INPUT_CATEGORIES_REGISTRATION_MESSAGE = Введите категории трат.

    Например: Продукты, Транспорт, Одежда

    Как закончите заполнять, нажмите кнопку ниже.

    Если хотите изменить категории, то зайдите в настройки

INPUT_CATEGORIES_MESSAGE = Введите категории трат.

    Например: Продукты, Транспорт, Одежда

    Как закончите заполнять, нажмите кнопку ниже.

INPUT_NEXT_CATEGORY_MESSAGE = Введите следующую категорию.

    Если хотите закончить ввод, нажмите кнопку ниже.

INPUT_AMOUNT_MESSAGE = Введите количество затраченных { $currency }.

    Если хотите изменить валюту, то зайдите в настройки

INPUT_EXPENSE_NAME = Введите пожалуйста название для данного расхода.

INPUT_CUSTOM_PERIOD_START_DATE = Введите дату начала периода в формате ДД.ММ.ГГГГ.

    Например: 01.01.2021

INPUT_CUSTOM_PERIOD_END_DATE = Введите дату окончания периода в формате ДД.ММ.ГГГГ.

    Например: 31.12.2021



# OTHER PROMPT MESSAGES
REGISTRATION_REQUIRED = Для начала работы с ботом, пожалуйста, зарегистрируйтесь.

    For using the bot, please register.

CONFIRM_EXPENSE = 
    Пожалуйста, подтвердите введенные данные:

    Название: { $name }
    Категория: { $category_name }
    Сумма: { $amount } { $currency }

    Если все верно, нажмите кнопку "Добавить трату", иначе "Не добавлять трату".

CONFIRM_REMOVE_CATEGORY =
    Пожалуйста, подтвердите удаление категории:

    Категория: { $category_name }

    Если все верно, нажмите кнопку "Удалить категорию", иначе "Не удалять категорию".

CONFIRM_CURRENCY_CHANGE = 
    Пожалуйста, подтвердите изменение валюты:

    Валюта: { $currency }

    Если все верно, нажмите кнопку "Изменить валюту", иначе "Не изменять валюту".

# -----------------------------
# ✅ SUCCESS MESSAGES
# -----------------------------

EXPENSE_ADDED = Трата успешно добавлена!

CATEGORY_REMOVED = Категория успешно удалена!

REGISTRATION_SUCCESS = 
    Вы успешно зарегистрировались!
    Выбранный язык: { $language }
    Выбранная валюта: { $currency }
    Категории трат: { $categories }

CATEGORIES_ADDED_MESSAGE = Категории успешно добавлены!

CURRENCY_CHANGED = Валюта успешно изменена!

LANGUAGE_CHANGED = Язык успешно изменен!

# -----------------------------
# ⏳ WAITING MESSAGES
# -----------------------------
WAIT_FOR_CUSTOM_STATISTICS = Пожалуйста, подождите, идет подсчет статистики...

WAIT_FOR_MONTH_STATISTICS = Пожалуйста, подождите, идет подсчет статистики за месяц...

# -----------------------------
# ℹ️ OTHER TEXTS
# -----------------------------

START_MESSAGE = Рады приветствовать Вас в боте для отслеживания ваших трат!

CANCELLED_EXPENSE = Трата отменена.

CANCELLED_REMOVE_CATEGORY = Удаление категории отменено.

CANCELLED_CHANGE_CURRENCY = Изменение валюты отменено.

CUSTOM_STATISTICS_PAGE = Статистика по выбранным параметрам:
    Категория: { $category_name }
    Потрачено за период: 
    { $total_expenses }

CUSTOM_STATISTICS_CURRENCY_SUM = 
    - { $amount } { $currency }
# -----------------------------
# 🎛️ BUTTONS
# -----------------------------

# CANCEL/END BUTTON
MAIN_MENU_BUTTON = Главное меню
CATEGORY_END_BUTTON = Закончить ввод категорий

# MAIN MENU BUTTONS
ADD_EXPENSE_BUTTON = Добавить трату
SHOW_EXPENSES_BUTTON = Анализ трат
SETTINGS_MENU_BUTTON = Настройки бота

# ADD EXPENSE BUTTONS
CONFIRM_EXPENSE_BUTTON = Добавить трату
CANCEL_EXPENSE_BUTTON = Не добавлять трату

# SETTINGS MENU BUTTONS
CATEGORIES_SETTINGS_MENU_BUTTON = Настройки Категорий
CHANGE_CURRENCY_MENU_BUTTON = Изменить валюту
CHANGE_LANGUAGE_MENU_BUTTON = Изменить язык

# CATEGORY SETTINGS MENU BUTTONS
ADD_CATEGORY_BUTTON = Добавить категорию/и
REMOVE_CATEGORY_BUTTON = Удалить категорию/и

# REMOVE CATEGORY BUTTONS

CONFIRM_REMOVE_CATEGORY_BUTTON = Удалить категорию
CANCEL_REMOVE_CATEGORY_BUTTON = Не удалять категорию

# CHANGE CURRENCY BUTTONS

CONFIRM_CHANGE_CURRENCY_BUTTON = Изменить валюту
CANCEL_CHANGE_CURRENCY_BUTTON = Не изменять валюту

# STATISTICS MENU BUTTONS

SHOW_CUSTOM_EXPENSES_STATISTICS_BUTTON = Показать статистику по категориям и дате
SHOW_MONTH_EXPENSES_STATISTICS_BUTTON = Показать статистику за месяц

# CUSTOM STATISTICS BUTTONS

DAY_PERIOD_BUTTON = За день
WEEK_PERIOD_BUTTON = За неделю
MONTH_PERIOD_BUTTON = За месяц
YEAR_PERIOD_BUTTON = За год
ALL_PERIOD_BUTTON = За все время
CUSTOM_PERIOD_BUTTON = За произвольный период

ALL_CATEGORIES_BUTTON = Все категории
END_CATEGORIES_SELECT_BUTTON = Закончить выбор категорий