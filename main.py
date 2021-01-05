import discord
from src.libs import database_handler
from src.commands import random_word, me_message, get_help, random_number

TOKEN = database_handler.get_data_from_database('tokens', 'bot_token')
SELECTED_BOT = database_handler.get_data_from_database('variables', 'currentSelectedBot')[0]
ACTIVITY_NAME = 'Helltaker'
client = discord.Client()


@client.event
async def on_ready():
	database_handler.clear_data_on_execution()
	for guild in client.guilds:
		async for member in guild.fetch_members(limit=None):
			if member.bot:
				database_handler.add_data_to_database('bots', ['bots_id'], [str(member.id)])
			else:
				database_handler.add_data_to_database('users', ['users_id'], [str(member.id)])
	await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=ACTIVITY_NAME))
	print(f'Successfully logged in as {client.user}!\nSet {ACTIVITY_NAME} as an activity')


@client.event
async def on_member_join(member):
	if member.bot:
		database_handler.add_data_to_database('bots', ['bots_id'], [str(member.id)])
	else:
		database_handler.add_data_to_database('users', ['users_id'], [str(member.id)])


@client.event
async def on_message(message):
	if message.author == client.user:
		return
	args = message.content.split(' ')
	command = args.pop(0).lower()
	if command in ('ху', 'who'):
			await random_word.get_random_word(message, args)
	elif command == 'йа':
			await me_message.send_me_message(message, args)
	elif command == 'хелп':
			await get_help.send_help_message(message)
	elif command == 'рандом':
			await random_number.get_random_number(message, args)
	else:
			return

client.run(TOKEN[int(SELECTED_BOT)])
