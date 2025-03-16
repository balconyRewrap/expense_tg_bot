"""Module contains exception classes for database module."""


class NotFoundError(Exception):
    """Exception raised when a database search returns no results.

    This exception should be used to indicate that a search for an object in the database
    has returned no results.
    """


class UserConfigNotFoundError(NotFoundError):
    """Raised when user config not found in db."""


class CategoryNotFoundError(NotFoundError):
    """Raised when category not found in db."""


class UserNotFoundError(NotFoundError):
    """Exception raised when a user is not found in the database.

    This exception is a subclass of NotFoundError and is used to indicate
    that a specific user could not be located within the database.
    """


class ExpenseNotFoundError(NotFoundError):
    """Raised when expense not found in db."""


class UniqueDublicateError(Exception):
    """Exception raised when a unique constraint is violated in the database."""
