"""secondthunder-py-bot.

This is a Discord bot script that runs on the Discord.py library and
allows you to execute functions using specific text commands

There is the starting point of the bot control, from where it begin its
work. Here you can change the entire logic of the bot and adjust it to
fit your needs
"""


import discord
from src.libs.database_handler import clear_data_on_execution
from src.libs.database_handler import get_data_from_database
from src.libs.database_handler import add_data_to_database
from src.commands.ded_makar import send_ded_makar_message
from src.commands.get_help import send_help_message
from src.commands.me_message import send_me_message
from src.commands.random_number import get_random_number
from src.commands.random_word import get_random_word


TOKEN = get_data_from_database('tokens', 'bot_token')
SELECTED_BOT = get_data_from_database('variables', 'current_selected_bot')[0]
ACTIVITY_NAME = 'Helltaker'
client = discord.Client()


@client.event
async def on_ready():
    """Execute necessary functions during the bot launch."""
    print('Clearing database...')
    clear_data_on_execution()
    print('Fetching all guild members...')
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            if member.bot:
                table = 'bots'
                key = 'bots_id'
            else:
                table = 'users'
                key = 'users_id'
            add_data_to_database(table, key, str(member.id))
    print(f'Setting \'{ACTIVITY_NAME}\' as an activity...')
    await client.change_presence(status=discord.Status.dnd,
                                 activity=discord.Game(name=ACTIVITY_NAME))
    print(f'Successfully logged in as {client.user}!')


@client.event
async def on_member_join(member):
    """Add new server users to the database while the bot is running.

    Parameters:
        member: Information about the user who joined the server
    """
    if member.bot:
        add_data_to_database('bots', 'bots_id', member.id)
    else:
        add_data_to_database('users', 'users_id', member.id)


@client.event
async def on_message(message):
    """Check for message and execute the function if the conditions are met.

    **Noteworthy:** If a bot receives a message from another bot or from itself, or does
    not receive the required command from the user, it does nothing

    Parameters:
        message (discord.message.Message): User message to perform required functions
    """
    if message.author == client.user:
        return
    args = message.content.split(' ')
    command = args.pop(0).lower()
    if command in ('ху', 'who'):
        await get_random_word(message, args)
    elif command == 'йа':
        await send_me_message(message, args)
    elif command == 'хелп':
        await send_help_message(message)
    elif command == 'рандом':
        await get_random_number(message, args)
    elif command == 'макар':
        await send_ded_makar_message(message, args)
    else:
        return

client.run(TOKEN[int(SELECTED_BOT)])
