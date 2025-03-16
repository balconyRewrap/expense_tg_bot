"""Module provides functions to initialize and reset the database."""
from database.config import engine
from database.models import Base


async def init_db() -> None:
    """Initialize the database by creating all tables defined in the metadata.

    This function asynchronously connects to the database engine, creates all
    tables defined in the Base metadata, and then disposes of the engine.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def reset_database() -> None:
    """Reset the database by dropping all tables and recreating them.

    This function asynchronously connects to the database engine, drops all
    tables defined in the Base metadata, and then recreates them before
    disposing of the engine.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


if __name__ == "__main__":
    # TODO(balconyRewrap): delete after debugging
    import asyncio  # noqa: WPS433
    asyncio.run(reset_database())
