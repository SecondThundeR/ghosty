import discord
from src.commands.randomWord import randomWord
from src.commands.meMessage import meMessage
from src.commands.getHelp import getHelp
from src.libs.dataImport import dataImport
from src.libs.databaseHandler import clearDataOnExecution, addDataToDatabase

TOKEN = dataImport('src/data/token.txt')
ACTIVITY_NAME = 'Helltaker'

client = discord.Client()


@client.event
async def on_ready():
    clearDataOnExecution()
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            if member.bot:
                addDataToDatabase('bots', ['bots_id'], [str(member.id)])
            else:
                addDataToDatabase('users', ['users_id'], [str(member.id)])
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=ACTIVITY_NAME))
    print(f'Successfully logged in as {client.user}!'
          f'\nSet {ACTIVITY_NAME} as an activity')


@client.event
async def on_member_join(member):
    if member.bot:
        addDataToDatabase('bots', ['bots_id'], [str(member.id)])
    else:
        addDataToDatabase('users', ['users_id'], [str(member.id)])


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
