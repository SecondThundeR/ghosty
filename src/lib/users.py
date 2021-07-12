"""User Handler Library.

This script allows to select user from list of server users
and get his information

This file can also be imported as a module and contains the following functions:
    * get_random_user - returns info of randomly chosen user
    * get_shipping_users - returns info of two randomly chosen users
    * get_members_name - returns nickname or name of member as a string
    * add_member_to_db - adds member to database
    * rem_member_from_db - removes member from database
    * is_user_admin - returns True, if user is admin of bot
    * is_user_blocked - returns True, if user is in blacklist of bot
"""


import random
import src.lib.database as database
from src.lib.exceptions import UsersNotFound


async def get_random_user(msg):
    """Get a random user from an list and return it's info.

    Args:
        msg (discord.message.Message): Info about guild from message

    Returns:
        discord.member.Member: Object with info about member
            which was randomly chosen.

    Raises:
        UsersNotFound: If list of users is empty
    """
    users = database.get_data(
        'mainDB',
        False,
        'SELECT users_id FROM users'
    )
    if users:
        member = await msg.guild.fetch_member(random.choice(users))
        return member
    raise UsersNotFound("В базе данных нет пользователей")


async def get_shipping_users(msg):
    """Get two random users from an list and return their info.

    Args:
        msg (discord.message.Message): Info about guild from message

    Returns:
        list: Users objects with their info which was randomly chosen

    Raises:
        UsersNotFound: If list of users is empty
    """
    users = database.get_data(
        'mainDB',
        False,
        'SELECT users_id FROM users'
    )
    if len(users) > 2:
        first_member = await msg.guild.fetch_member(
            first_member_id := random.choice(users)
        )
        users.remove(first_member_id)
        second_member = await msg.guild.fetch_member(random.choice(users))
        return [first_member, second_member]
    raise UsersNotFound("В базе данных недостаточно пользователей для шиппинга")


def get_members_name(member):
    """Check if member has a nickname on server.

    Args:
        member (discord.member.Member): Info about member of guild

    Returns:
        str: User's name, if user doesn't have a nickname and otherwise
    """
    return member.name if not member.nick else member.nick


def add_member_to_db(member):
    """Add member to database.

    Used for adding members on startup or when member is getting
    on the server

    Args:
        member (discord.member.Member): Info about member of guild
    """
    db_table = 'users' if not member.bot else 'bots'
    return database.modify_data(
        'mainDB',
        f'INSERT INTO {db_table} VALUES (?)',
        member.id
    )


def rem_member_from_db(member):
    """Remove member from database.

    Used for removing members from database in certain cases
    (Ignoring in shipping and etc.)

    **Noteworthy:** This makes sense until the bot reboots. In future there are plans
    for adding ignore list for shipping and other commands

    Args:
        member (discord.member.Member): Info about member of guild
    """
    if not member.bot:
        db_table, db_column = 'users', 'users_id'
    else:
        db_table, db_column = 'bots', 'bots_id'
    return database.modify_data(
        'mainDB',
        f'DELETE FROM {db_table} WHERE {db_column} = ?',
        member.id
    )


def is_user_admin(user_id):
    """Check if user is an admin of bot.

    Args:
        user_id (str): ID of user to check

    Returns:
        bool: True, if user is admin of bot. False otherwise
    """
    db_id = database.get_data(
        'mainDB',
        False,
        'SELECT admins_id FROM admin_list WHERE admins_id = ?',
        user_id
    )
    return int(user_id) in db_id


def is_user_blocked(user_id):
    """Check if user is in blacklist of bot.

    Args:
        user_id (str): ID of user to check

    Returns:
        bool: True, if user is banned. False otherwise
    """
    db_id = database.get_data(
        'mainDB',
        False,
        'SELECT blocked_id FROM block_list WHERE blocked_id = ?',
        user_id
    )
    return int(user_id) in db_id
