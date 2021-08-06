"""User Handler Library.

This script allows to select user from list of server users
and get his information

This file can also be imported as a module and contains the following functions:
    * get_random_user - returns info of randomly chosen user
    * get_shipping_users - returns info of two randomly chosen users
    * get_members_name - returns nickname or name of member as a string
    * add_member_to_db - adds member to database
    * add_bot_to_db - adds bot to database
    * rem_member_from_db - removes member from database
    * is_user_admin - returns True, if user is admin of bot
    * is_user_blocked - returns True, if user is in blacklist of bot
"""


import random
import src.lib.database as database
from src.lib.exceptions import UsersNotFound


def _get_users_list():
    """Get and return list of users ids.

    Returns:
        list: Array of users ids from DB
    """
    return database.get_data(
        'mainDB',
        False,
        'SELECT users_id FROM users'
    )


def _get_admin_status(user_id):
    """Get user_id and compares with one in DB.

    Args:
        user_id (str): ID of user to check

    Returns:
        bool: True, if compare successful. False otherwise
    """
    return database.get_data(
        'mainDB',
        False,
        'SELECT admins_id FROM admin_list WHERE admins_id = ?',
        user_id
    ) == int(user_id)


def _get_block_status(user_id):
    """Get user_id and compares with one in DB.

    Args:
        user_id (str): ID of user to check

    Returns:
        bool: True, if compare successful. False otherwise
    """
    return database.get_data(
        'mainDB',
        False,
        'SELECT blocked_id FROM block_list WHERE blocked_id = ?',
        user_id
    ) == int(user_id)


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
    users = _get_users_list()
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
    users = _get_users_list()
    if len(users) >= 2:
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
        member (Union[discord.member.Member, list]): Info about member of guild

    Returns:
        str: User's name, if user doesn't have a nickname and otherwise
        list: List of names of user's nicknames
    """
    if type(member) is list:
        members_data = []
        for m in member:
            members_data.append(m.name if not m.nick else m.nick)
        return members_data
    return member.name if not member.nick else member.nick


def add_member_to_db(member_id):
    """Add member to database.

    Used for adding members on startup or when member is getting
    on the server

    Args:
        member_id (int): ID of member to add
    """
    return database.modify_data(
        'mainDB',
        'INSERT INTO users VALUES (?)',
        member_id
    )


def add_bot_to_db(bot_id):
    """Add bot to database.

    Used for adding bots on startup or when member is getting
    on the server (For some ignore purposes)

    Args:
        bot_id (int): ID of bot to add
    """
    return database.modify_data(
        'mainDB',
        'INSERT INTO bots VALUES (?)',
        bot_id
    )


def rem_member_from_db(member_id):
    """Remove member from database.

    Used for removing members from database in certain cases
    (Ignoring in shipping and etc.)

    **Noteworthy:** This makes sense until the bot reboots. In future there are plans
    for adding ignore list for shipping and other commands

    Args:
        member_id (int): ID of member to remove
    """
    return database.modify_data(
        'mainDB',
        'DELETE FROM users WHERE users_id = ?',
        member_id
    )


def is_user_admin(user_id):
    """Check if user is an admin of bot.

    Args:
        user_id (str): ID of user to check

    Returns:
        bool: True, if user is admin of bot. False otherwise
    """
    return _get_admin_status(user_id)


def is_user_blocked(user_id):
    """Check if user is in blacklist of bot.

    Args:
        user_id (str): ID of user to check

    Returns:
        bool: True, if user is banned. False otherwise
    """
    return _get_block_status(user_id)
