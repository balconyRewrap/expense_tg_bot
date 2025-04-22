💸 Expense Tracker Bot
=======================

A multilingual Telegram bot to **track your expenses** with ease.  
Supports **English** and **Russian** languages.

**Documentation**: `GitHub Pages <https://balconyrewrap.github.io/expense_tg_bot/>`_

----

🚀 Features
-----------

- Track expenses over various **time periods**.
- Create and manage your own **custom categories**.
- View detailed summaries of your spending.
- Localized in **English and Russian**.

----

⚙️ Setup Instructions
---------------------

1. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

Make sure you have `uv <https://github.com/astral-sh/uv>`_ installed:

.. code-block:: bash

   pip install uv

Then, install all project dependencies:

.. code-block:: bash

   uv sync

----

2. Database Requirements
~~~~~~~~~~~~~~~~~~~~~~~~

This bot uses **PostgreSQL** and **Redis**. Please ensure both services are installed and running.

**PostgreSQL Setup**

- Create a **user** and a **database** manually in PostgreSQL.

**Redis Setup**

- Ensure Redis is up and running on the host and port you plan to use.

----

3. Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~

Set the following variables in a `.env` file or directly in your environment:

.. code-block:: env

   API_TOKEN=your_telegram_token_from_BotFather

   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0

   PGSQL_HOST=localhost
   PGSQL_PORT=5432
   PGSQL_DB=your_database_name
   PGSQL_USER=your_postgres_user
   PGSQL_PASSWORD=your_postgres_password

----

4. Initialize the Database
~~~~~~~~~~~~~~~~~~~~~~~~~~

Before running the bot, initialize the PostgreSQL schema:

.. code-block:: bash

   uv run run_bot.py --init-db

----

5. Run the Bot
~~~~~~~~~~~~~~

Once everything is set up:

.. code-block:: bash

   uv run run_bot.py

----

🌍 Localization
---------------

- **en** English
- **ru** Russian

----

🧩 Contributing
---------------

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

----

🛡️ License
-----------

This project is licensed under the MIT License.

----

📬 Questions or issues?
-----------------------

Feel free to open an issue.


.. toctree::
   :maxdepth: 8
   :caption: Contents:

   pages/index.rst


