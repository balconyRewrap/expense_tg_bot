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

# NOT GOTTEN ERROR
ERROR_CURRENCY = Ошибка: не удалось получить выбранную валюту.

ERROR_CATEGORIES = Ошибка: не удалось получить категорию.

ERROR_USER_CURRENCY = 
    Ошибка: не удалось получить выбранную валюту.

    Возможно у вас не выбрана валюта, выберите, пожалуйста в настройках.
# INFO FROM DB ERROR
ERROR_NO_CATEGORIES = 
    Ошибка: у вас нет категорий.

    Пожалуйста, добавьте категории в настройках.

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

# INPUT PROMPT MESSAGES
INPUT_CURRENCY_MESSAGE = Введите валюту, которую хотите использовать.

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

# OTHER PROMPT MESSAGES
REGISTRATION_REQUIRED = Для начала работы с ботом, пожалуйста, зарегистрируйтесь.

    For using the bot, please register.

CONFIRM_EXPENSE = 
    Пожалуйста, подтвердите введенные данные:

    Название: { $name }
    Категория: { $category_name }
    Сумма: { $amount } { $currency }

    Если все верно, нажмите кнопку "Добавить трату", иначе "Не добавлять трату".

# -----------------------------
# ✅ SUCCESS MESSAGES
# -----------------------------

EXPENSE_ADDED = Трата успешно добавлена!

REGISTRATION_SUCCESS = 
    Вы успешно зарегистрировались!
    Выбранный язык: { $language }
    Выбранная валюта: { $currency }
    Категории трат: { $categories }

CATEGORIES_ADDED_MESSAGE = Категории успешно добавлены!

# -----------------------------
# ℹ️ OTHER TEXTS
# -----------------------------

START_MESSAGE = Рады приветствовать Вас в боте для отслеживания ваших трат!

CANCELLED_EXPENSE = Трата отменена.

# -----------------------------
# 🎛️ BUTTONS
# -----------------------------

# CANCEL/END BUTTON
MAIN_MENU_BUTTON = Главное меню
CATEGORY_END_BUTTON = Закончить ввод категорий

# MAIN MENU BUTTONS
ADD_EXPENSE_BUTTON = Добавить трату
SHOW_EXPENSES_BUTTON = Показать траты за определенное время
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