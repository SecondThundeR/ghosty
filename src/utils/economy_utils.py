import src.lib.database as database


DEFAULT_BALANCE = 1000


def check_account(user_id):
    account_status = database.get_data(
        'pointsDB',
        True,
        'SELECT * FROM points WHERE user_id = ?',
        user_id
    )
    return bool(account_status)


def add_new_account(user_id):
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
