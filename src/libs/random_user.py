import random
from src.libs import database_handler

users = database_handler.get_data_from_database('users', ['users_id'])


async def get_random_user(msg, mode='default'):
	"""Get random user object from users id

	Parameters:
		msg: Info about guild from message
		mode (str): Mode of getting random user. When 'shipping' is selected, executing different statement
		for getting two random users. Defaults to 'default'

	Returns:
		Info about member which was randomly chosen. None for empty array of users
	"""
	if users is None:
		return users
	if mode == 'shipping':
		return 'Not implemented'
	member = await msg.guild.fetch_member(random.choice(users))
	return member
