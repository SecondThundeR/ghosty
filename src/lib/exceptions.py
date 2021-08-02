"""Custom Exceptions.

This file stores all custom exceptions used in the project.

In future, there can be added new exceptions.
"""


class CustomErrors(Exception):
    """Base class for other exceptions"""


class UsersNotFound(CustomErrors):
    """Raised when users cannot be found in database"""


class WordsImportError(CustomErrors):
    """Raised when words base imported with failure"""
