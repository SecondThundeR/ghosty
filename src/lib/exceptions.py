class CustomErrors(Exception):
    """Base class for other exceptions"""
    pass

class UsersNotFound(CustomErrors):
    """Raised when users cannot be found in database"""
    pass