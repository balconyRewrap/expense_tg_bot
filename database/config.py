"""Module configures the database connection for the tg_bot_funko project.

It uses environment variables to set up the PostgreSQL database connection
parameters and creates an asynchronous SQLAlchemy engine and session maker.

Attributes:
    PGSQL_HOST: The hostname of the PostgreSQL server.
    PGSQL_PORT: The port number of the PostgreSQL server.
    PGSQL_DB: The name of the PostgreSQL database.
    PGSQL_USER: The username for the PostgreSQL database.
    PGSQL_PASSWORD: The password for the PostgreSQL database.
    DATABASE_URL (str): The constructed database URL for the PostgreSQL connection.
    engine (sqlalchemy.ext.asyncio.AsyncEngine): The asynchronous SQLAlchemy engine.
    async_session_maker (sqlalchemy.ext.asyncio.async_sessionmaker): The asynchronous session maker.
"""
from decouple import config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

PGSQL_HOST = config("PGSQL_HOST")
PGSQL_PORT = config("PGSQL_PORT")
PGSQL_DB = config("PGSQL_DB")
PGSQL_USER = config("PGSQL_USER")
PGSQL_PASSWORD = config("PGSQL_PASSWORD")

DATABASE_URL = (
    f"postgresql+asyncpg://{PGSQL_USER}:{PGSQL_PASSWORD}@"
    f"{PGSQL_HOST}:{PGSQL_PORT}/{PGSQL_DB}"  # noqa: WPS221
)

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
