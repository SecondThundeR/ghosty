"""Utils for server's economy.

This utils contains all needed functions to handle economy operations
between users or certain commands.

This file can also be imported as a module and contains the following functions:
    * check_account - checks is a user points account exists
    * add_new_account - adds new points account to DB
    * delete_account - deletes active points acccount from DB
    * get_account_balance - returns balance of a user account
    * tranfer_points - transfers points between two points accounts
"""

import src.lib.database as database


# Initial values for points accounts
# Can be changed later on
DEFAULT_BALANCE = 1000


def check_account(user_id):
    """Check if points account exists.

    Args:
        user_id (int): The ID of ther user

    Returns:
        bool: True if account exists, False otherwise.
    """
    account_status = database.get_data(
        'pointsDB',
        True,
        'SELECT * FROM points WHERE user_id = ?',
        user_id
    )
    return bool(account_status)


def add_new_account(user_id):
    """Add new points accounts to database.

    Args:
        user_id (int): The ID of the user

    Returns:
        bool: True if account was added, False if account is already added
    """
    account_status = check_account(user_id)
    if account_status:
        return False
    database.modify_data(
        'pointsDB',
        'INSERT INTO points VALUES (?, ?)',
        user_id, DEFAULT_BALANCE
    )
    return True


def delete_account(user_id):
    """Remove active points account from database.

    Args:
        user_id (int): The ID of the user

    Returns:
        bool: True if account was deleted, False if account was already deleted
    """
    account_status = check_account(user_id)
    if not account_status:
        return False
    database.modify_data(
        'pointsDB',
        'DELETE FROM points WHERE user_id = ?',
        user_id
    )
    return True


def get_account_balance(user_id):
    """Get balance of user points account.

    Args:
        user_id (int): The ID of the user

    Returns:
        int: The balance of the user account
        None: If the user does not have an account
    """
    account_status = check_account(user_id)
    if not account_status:
        return None
    user_account = database.get_data(
        'pointsDB',
        True,
        'SELECT points_balance FROM points WHERE user_id = ?',
        user_id
    )
    return user_account


def transfer_points(sender_id, reciever_id, points):
    """Manage transferring points balance between two points accounts.

    Args:
        sender_id (int): The ID of the sender
        reciever_id (int): The ID of the reciever
        points (int): The amount of points to transfer
    """
    sender_balance = get_account_balance(sender_id)
    if sender_balance - points <= 0:
        return False
    database.modify_data(
        'pointsDB',
        'UPDATE points SET points_balance = points_balance - ? WHERE user_id = ?',
        points, sender_id
    )
    database.modify_data(
        'pointsDB',
        'UPDATE points SET points_balance = points_balance + ? WHERE user_id = ?',
        points, reciever_id
    )
    return True
