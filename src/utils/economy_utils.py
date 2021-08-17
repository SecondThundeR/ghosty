"""Utils for server's economy.

This utils contains all needed functions to handle economy operations
between users or certain commands.

This file can also be imported as a module and contains the following functions:
    * check_account - checks is a user points account exists
    * add_new_account - adds new points account to DB
    * delete_account - deletes active points acccount from DB
    * get_account_balance - returns balance of a user account
    * tranfer_points - transfers points between two points accounts
    * add_points - adds points to a user points account
    * subtract_points - subtracts points from a user points account
    * daily_points_manager - manages getting and giving daily points
"""

import random
import datetime as dt
import src.lib.database as database


# Initial values for points accounts
# Can be changed later on
DEFAULT_BALANCE = 1000
# Set, if account was deleted previously
# This will prevent abusing the system
# by getting infinite points (1000 on each account creation)
# Check for deleted account will be implemented later
ZERO_BALANCE = 0


def check_account(user_id):
    """Check if points account exists.

    Args:
        user_id (int): The ID of ther user

    Returns:
        None: If account does not exist
        bool: True if account exists, False if account deleted.
    """
    account_status = database.get_data(
        'pointsDB',
        True,
        'SELECT is_deleted FROM points_accounts WHERE user_id = ?',
        user_id
    )
    if account_status is None:
        return None
    if account_status == 1:
        return False
    return True


def add_new_account(user_id):
    """Add new points accounts to database.

    Args:
        user_id (int): The ID of the user

    Returns:
        None: If account wasn't created previously
        bool: True if account was restored, False if account is already added
    """
    account_status = check_account(user_id)
    if account_status:
        return False
    if account_status is None:
        database.modify_data(
            'pointsDB',
            'INSERT INTO points_accounts VALUES (?, ?, 0, "")',
            user_id, DEFAULT_BALANCE
        )
        return None
    database.modify_data(
        'pointsDB',
        'UPDATE points_accounts SET is_deleted = 0 WHERE user_id = ?',
        user_id
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
        'UPDATE points_accounts SET points_balance = ?, '
        'is_deleted = 1 WHERE user_id = ?',
        ZERO_BALANCE, user_id
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
        'SELECT points_balance FROM points_accounts WHERE user_id = ?',
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
    subtract_points(sender_id, points, skip_check=True)
    add_points(reciever_id, points, skip_check=True)
    return True


def add_points(user_id, points, skip_check=False):
    """Add points to user points account.

    Args:
        user_id (int): The ID of the user
        points (int): The amount of points to add
        skip_check (bool): Skip checking if check was already done
    """
    if not skip_check:
        account_status = check_account(user_id)
        if not account_status:
            return False
    database.modify_data(
        'pointsDB',
        'UPDATE points_accounts '
        'SET points_balance = points_balance + ? WHERE user_id = ?',
        points, user_id
    )
    return True


def subtract_points(user_id, points, skip_check=False):
    """Subtract points from user points account.

    Args:
        user_id (int): The ID of the user
        points (int): The amount of points to subtract
        skip_check (bool): Skip checking if check was already done
    """
    if not skip_check:
        account_status = check_account(user_id)
        if not account_status:
            return False
    account_balance = get_account_balance(user_id)
    if account_balance == 0 or account_balance < points:
        return False
    database.modify_data(
        'pointsDB',
        'UPDATE points_accounts '
        'SET points_balance = points_balance - ? WHERE user_id = ?',
        points, user_id
    )
    return True


def daily_points_manager(user_id):
    """Manage daily points rewarding.

    Args:
        user_id (int): The ID of the user

    Returns:
        int: The amount of bouns points
        bool: False if points accounts does not exist
        None: If user alredy got daily points
    """
    account_status = check_account(user_id)
    if not account_status:
        return False
    current_date = dt.datetime.now().date()
    next_date = (dt.datetime.now() + dt.timedelta(days=1)).date()
    daily_points_date = database.get_data(
        'pointsDB',
        True,
        'SELECT daily_points_date FROM points_accounts WHERE user_id = ?',
        user_id
    )
    if not daily_points_date or current_date >= dt.datetime.strptime(
        daily_points_date, '%Y-%m-%d'
    ).date():
        random_points = random.randrange(100, 2000, 100)
        add_points(user_id, random_points, skip_check=True)
        database.modify_data(
            'pointsDB',
            'UPDATE points_accounts SET daily_points_date = ? '
            'WHERE user_id = ?',
            next_date, user_id
        )
        return random_points
    if current_date < dt.datetime.strptime(daily_points_date, '%Y-%m-%d').date():
        return None
