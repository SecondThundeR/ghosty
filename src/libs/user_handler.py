"""Library for obtaining information about a randomly selected user.

This script allows to select a random user from list of server users
and get his information

This file can also be imported as a module and contains the following functions:
    * get_random_user - returns info of randomly chosen user
    * get_members_name - returns nickname or name of member as a string
"""


import random
from src.libs.database_handler import get_data_from_database

users = get_data_from_database('users', 'users_id')


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
    if users is None:
        return users
    if mode == 'shipping':
        return 'Not implemented'
    member = await msg.guild.fetch_member(random.choice(users))
    return member


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
