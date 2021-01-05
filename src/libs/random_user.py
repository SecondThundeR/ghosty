import random
from src.libs import database_handler

users = database_handler.get_data_from_database('users', ['users_id'])


async def get_random_user(msg, mode='default'):
    if mode == 'shipping':
        return 'Not implemented'
    member = await msg.guild.fetch_member(random.choice(users))
    return member
