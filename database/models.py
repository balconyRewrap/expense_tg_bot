"""Module defines the database models for the application using SQLAlchemy."""
from sqlalchemy import BigInteger, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all database models.

    This class inherits from AsyncAttrs and DeclarativeBase, providing
    asynchronous attributes and declarative base functionality for SQLAlchemy models.
    """


class Expense(Base):
    """Represent an expense record in the database.

    Attributes:
        id (int): The primary key of the expense.
        name (str): The name or description of the expense.
        currency (str): The currency in which the expense is made.
        amount (int): The amount of the expense.
        date (datetime.date): The date when the expense was made.
        user_tg_id (int): The Telegram user ID associated with the expense.
        user (User): The user who made the expense.
        category_id (int): The ID of the category to which the expense belongs.
        category (Category): The category of the expense.
    """

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)  # noqa: VNE003
    name = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    user_tg_id = Column(BigInteger, ForeignKey("users.user_tg_id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="expenses")

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="expenses")


class User(Base):
    """Represent a user in the database.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        user_tg_id (BigInteger): The primary key representing the user's Telegram ID.
        expenses (relationship): A relationship to the Expense model, representing the user's expenses.
        config (relationship): A one-to-one relationship to the UserConfig model, representing the user's configuration.
    """

    __tablename__ = "users"

    user_tg_id = Column(BigInteger, primary_key=True)

    expenses = relationship("Expense", back_populates="user")

    config = relationship("UserConfig", uselist=False, back_populates="user")


class UserConfig(Base):
    """Represent the configuration settings for a user.

    Attributes:
        user_tg_id (BigInteger): Telegram user ID, primary key, and foreign key referencing users.user_tg_id.
        language (String): The language preference of the user.
        currency (String): The currency preference of the user.
        user (relationship): Relationship to the User model, back_populated by the 'config' attribute.
        categories (relationship):
            Relationship to the Category model, back_populated by the 'config' attribute, with cascade delete-orphan.
    """

    __tablename__ = "user_configs"

    user_tg_id = Column(BigInteger, ForeignKey("users.user_tg_id"), primary_key=True)
    language = Column(String, nullable=False)
    currency = Column(String, nullable=False)

    user = relationship("User", back_populates="config")
    categories = relationship("Category", back_populates="config", cascade="all, delete-orphan")


class Category(Base):
    """Represents a category of expenses.

    Attributes:
        id (int): The unique identifier of the category.
        name (str): The name of the category (e.g., "Food", "Transport").
        config_id (int): The foreign key referencing the user configuration.
        config (UserConfig): The relationship to the UserConfig model.
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)  # noqa: VNE003
    name = Column(String, nullable=False)
    config_id = Column(BigInteger, ForeignKey("user_configs.user_tg_id", ondelete="CASCADE"), nullable=False)
    config = relationship("UserConfig", back_populates="categories")

    expenses = relationship("Expense", back_populates="category")
