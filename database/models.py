"""This module defines the database models for the application using SQLAlchemy."""
from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all database models.

    This class inherits from AsyncAttrs and DeclarativeBase, providing
    asynchronous attributes and declarative base functionality for SQLAlchemy models.
    """


class Expense(Base):
    """A model representing an expense in the database.

    Attributes:
        id (int): The primary key for the expense.
        user_tg_id (int): The ID of the user who created the expense.
        name (str): The name of the expense.
        currency (str): The currency of the expense.
        amount (float): The amount of the expense.
        date (datetime.date): The date of the expense.
        is_deleted (bool): A flag indicating if the expense has been deleted.
    """

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)  # noqa: VNE003
    user_tg_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, default=False)


class UserConfig(Base):
    """A model representing a config for tg user in bot.

    Attributes:
        user_tg_id (int): the primary key, tg id of user.
        language (str): language of user.
        currency (str): user currency of expenses.
        categories (relation ship to Categories table): user's categories of expenses.
    """

    __tablename__ = "user_configs"

    user_tg_id = Column(BigInteger, primary_key=True)
    language = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    categories = relationship("Category", back_populates="config", cascade="all, delete-orphan")


class Category(Base):
    """Represents a category of expenses.

    Attributes:
        id (int): The unique identifier of the category.
        name (str): The name of the category (e.g., "Food", "Transport").
        config_id (int): The foreign key referencing the user configuration.
        config (UserConfig): The relationship to the UserConfig model.
    """

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)  # noqa: VNE003
    name = Column(String, nullable=False)
    config_id = Column(Integer, ForeignKey('user_configs.id', ondelete="CASCADE"), nullable=False)
    config = relationship("UserConfig", back_populates="categories")
