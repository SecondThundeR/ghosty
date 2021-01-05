import discord
from src.commands.randomWord import randomWord
from src.commands.meMessage import meMessage
from src.commands.getHelp import getHelp
from src.libs.dataImport import dataImport
from src.libs.database_handler import clear_data_on_execution, add_data_to_database

TOKEN = dataImport('src/data/token.txt')
ACTIVITY_NAME = 'Helltaker'

client = discord.Client()


@client.event
async def on_ready():
    clear_data_on_execution()
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            if member.bot:
                add_data_to_database('bots', ['bots_id'], [str(member.id)])
            else:
                add_data_to_database('users', ['users_id'], [str(member.id)])
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=ACTIVITY_NAME))
    print(f'Successfully logged in as {client.user}!'
          f'\nSet {ACTIVITY_NAME} as an activity')


@client.event
async def on_member_join(member):
    if member.bot:
        add_data_to_database('bots', ['bots_id'], [str(member.id)])
    else:
        add_data_to_database('users', ['users_id'], [str(member.id)])


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    args = message.content.split(' ')
    command = args.pop(0).lower()
    if command == 'ху' or command == 'who':
        await randomWord(message, args)
    elif command == 'йа':
        await meMessage(message, args)
    elif command == 'хелп':
        await getHelp(message)
    else:
        return

client.run(TOKEN[0])
