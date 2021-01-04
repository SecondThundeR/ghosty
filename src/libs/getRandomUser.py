import random
from src.libs.databaseHandler import getDataFromDatabase
users = getDataFromDatabase('users', ['users_id'])


async def getRandomUser(msg, mode='default'):
    if mode == 'shipping':
        pass
    member = await msg.guild.fetch_member(random.choice(users))
    return member
