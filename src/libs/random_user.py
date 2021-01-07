"""Library for obtaining information about a randomly selected user

This script allows to select a random user from list of server users
and get his information

This file can also be imported as a module and contains the following functions:
    * get_random_user - return info of randomly chosen user
"""


import random
from src.libs.database_handler import get_data_from_database

users = get_data_from_database('users', ['users_id'])


async def get_random_user(msg, mode='default'):
    """Getting a random user from an list and returning user's info

    Parameters:
        msg: Info about guild from message
        mode (str): Mode of getting random user.
        When 'shipping' is selected, executing different statement for getting
        two random users. Defaults to 'default'

    Returns:
        User object about member which was randomly chosen.
            None for empty array of users
    """
    if users is None:
        return users
    if mode == 'shipping':
        return 'Not implemented'
    member = await msg.guild.fetch_member(random.choice(users))
    return member
