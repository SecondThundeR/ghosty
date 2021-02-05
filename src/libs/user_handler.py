"""Library for obtaining information about users.

This script allows to select user from list of server users
and get his information

This file can also be imported as a module and contains the following functions:
    * get_random_user - returns info of randomly chosen user
    * get_members_name - returns nickname or name of member as a string
    * is_user_admin - returns True, if user is admin of bot
"""


import random
from src.libs.database_handler import is_data_in_database
from src.libs.database_handler import get_data_from_database


async def get_random_user(msg, mode='default'):
    """Get a random user from an list and returning user's info.

    Parameters:
        msg (discord.message.Message): Info about guild from message
        mode (str): Mode of getting random user.
        When 'shipping' is selected, executing different statement for getting
        two random users. Defaults to 'default'

    Returns:
        discord.member.Member: User object about member
            which was randomly chosen.
        None for empty array of users
    """
    users = get_data_from_database(0, 'users', 'users_id')
    if mode == 'shipping':
        try:
            first_member = await msg.guild.fetch_member(random.choice(users))
            second_member = await msg.guild.fetch_member(random.choice(users))
            while second_member == first_member:
                second_member = await msg.guild.fetch_member(random.choice(users))
            return [first_member, second_member]
        except IndexError:
            return None
    try:
        member = await msg.guild.fetch_member(random.choice(users))
        return member
    except IndexError:
        return None


def get_members_name(member):
    """Check if member has a nickname on server.

    Parameters:
        member (discord.member.Member): Info about member of guild

    Returns:
        str: User's name, if user doesn't have a nickname and otherwise
    """
    if member.nick is None:
        return member.name
    return member.nick


def is_user_admin(msg):
    """Check if member has a nickname on server.

    Parameters:
        msg (discord.message.Message): Get ID of user's message

    Returns:
        bool: True, if user is admin of bot. False otherwise
    """
    return is_data_in_database(0,
                               'admin_list',
                               'admins_id',
                               msg.author.id)
