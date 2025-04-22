# 💸 Expense Tracker Bot | Бот для отслеживания расходов

A multilingual Telegram bot to **track your expenses** with ease.  
Supports **English** and **Russian** languages.

📖 **Documentation**: [GitHub Pages](https://balconyrewrap.github.io/expense_tg_bot/)

---

## 🚀 Features

- Track expenses over various **time periods**.
- Create and manage your own **custom categories**.
- View detailed summaries of your spending.
- Localized in **English and Russian**.

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

Make sure you have [uv](https://github.com/astral-sh/uv) installed:

```bash
pip install uv
```

Then, install all project dependencies:

```bash
uv sync
```

---

### 2. Database Requirements

This bot uses **PostgreSQL** and **Redis**. Please ensure both services are installed and running.

#### PostgreSQL Setup

- Create a **user** and a **database** manually in PostgreSQL.

#### Redis Setup

- Ensure Redis is up and running on the host and port you plan to use.

---

### 3. Environment Variables

Set the following variables in a `.env` file or directly in your environment:

```env
API_TOKEN=your_telegram_token_from_BotFather

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

PGSQL_HOST=localhost
PGSQL_PORT=5432
PGSQL_DB=your_database_name
PGSQL_USER=your_postgres_user
PGSQL_PASSWORD=your_postgres_password
```

---

### 4. Initialize the Database

Before running the bot, initialize the PostgreSQL schema:

```bash
uv run run_bot.py --init-db
```

---

### 5. Run the Bot

Once everything is set up:

```bash
uv run run_bot.py
```

---

## 🌍 Localization

- **en** English
- **ru** Russian

---

## 🧩 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

📬 Questions or issues? Feel free to open an issue.

---

# 💸 Бот для отслеживания расходов

Многоязычный Telegram-бот для **удобного отслеживания ваших расходов**.  
Поддерживает **английский** и **русский** языки.

📖 **Документация**: [GitHub Pages](https://balconyrewrap.github.io/expense_tg_bot/)

---

## 🚀 Возможности

- Отслеживайте расходы за различные **периоды времени**.
- Создавайте и управляйте своими **пользовательскими категориями**.
- Просматривайте подробные сводки по тратам.
- Локализация на **английском и русском** языках.

---

## ⚙️ Инструкции по установке

### 1. Установка зависимостей

Убедитесь, что установлен [uv](https://github.com/astral-sh/uv):

```bash
pip install uv
```

Затем установите все зависимости проекта:

```bash
uv sync
```

---

### 2. Требования к базе данных

Бот использует **PostgreSQL** и **Redis**. Убедитесь, что оба сервиса установлены и запущены.

#### Настройка PostgreSQL

- Создайте **пользователя** и **базу данных** вручную в PostgreSQL.

#### Настройка Redis

- Убедитесь, что Redis запущен на указанном хосте и порту.

---

### 3. Переменные окружения

Задайте следующие переменные в файле `.env` или напрямую в окружении:

```env
API_TOKEN=токен_вашего_бота_от_BotFather

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

PGSQL_HOST=localhost
PGSQL_PORT=5432
PGSQL_DB=название_вашей_базы
PGSQL_USER=пользователь_postgres
PGSQL_PASSWORD=пароль_postgres
```

---

### 4. Инициализация базы данных

Перед запуском бота необходимо инициализировать схему базы данных PostgreSQL:

```bash
uv run run_bot.py --init-db
```

---

### 5. Запуск бота

После завершения настройки:

```bash
uv run run_bot.py
```

---

## 🌍 Локализация

- **en** Английский
- **ru** Русский

---

## 🧩 Участие в разработке

Pull request'ы приветствуются! Для крупных изменений, пожалуйста, сначала откройте issue, чтобы обсудить ваши предложения.

---

## 🛡️ Лицензия

Этот проект лицензирован под [лицензией MIT](LICENSE).

---

📬 Вопросы или проблемы? Смело открывайте issue.
