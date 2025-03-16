"""Utility functions for database operations."""
from sqlalchemy.exc import IntegrityError


def is_unique_error(exception: IntegrityError) -> bool:
    """Check if the given IntegrityError is due to a unique constraint violation.

    Args:
        exception (IntegrityError): The exception to check.

    Returns:
        bool: True if the exception is a unique constraint violation, False otherwise.
    """
    return "UniqueViolationError" in str(exception)
