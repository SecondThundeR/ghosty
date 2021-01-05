import random
from src.libs.database_handler import get_data_from_database

users = get_data_from_database('users', ['users_id'])


async def getRandomUser(msg, mode='default'):
    if mode == 'shipping':
        pass
    member = await msg.guild.fetch_member(random.choice(users))
    return member
