"""secondthunder-py-bot.

This is a Discord bot script that runs on the Discord.py library and
allows you to execute functions using specific text commands

There is the starting point of the bot control, from where it begin its
work. Here you can change the entire logic of the bot and adjust it to
fit your needs
"""


import time
import discord as Discord
from src.libs.database_handler import clear_data_on_execution, edit_data_in_database
from src.libs.database_handler import get_data_from_database
from src.libs.database_handler import add_data_to_database
from src.commands.ded_makar import send_ded_makar_message
from src.commands.get_help import send_help_message
from src.commands.get_uptime import get_uptime_message
from src.commands.me_message import send_me_message
from src.commands.random_number import get_random_number
from src.commands.random_ship import ship_func_chooser
from src.commands.random_word import get_random_word
from src.commands.russian_roulette import start_roulette
from src.commands.system_info import get_system_info
from src.commands.user_checker import who_is_user


TOKENS = get_data_from_database(1, 'tokens', 'bot_token')
SELECTED_BOT = get_data_from_database(0, 'variables', 'current_selected_bot')[0]
ADMINS = get_data_from_database(0, 'admin_list', 'admins_id')
BLOCKED = get_data_from_database(0, 'block_list', 'blocked_id')
ACTIVITY_NAME = 'Helltaker'
intents = Discord.Intents.default()
intents.members = True
client = Discord.Client(intents=intents)


@client.event
async def on_ready():
    """Execute necessary functions during the bot launch."""
    clear_data_on_execution()
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            if member.bot:
                add_data_to_database(0, 'bots', 'bots_id', member.id)
            else:
                add_data_to_database(0, 'users', 'users_id', member.id)
    await client.change_presence(status=Discord.Status.dnd,
                                 activity=Discord.Game(name=ACTIVITY_NAME))
    print(f'Successfully logged in as {client.user}!')
    edit_data_in_database(0, 'variables', 'bot_uptime', int(time.time()))


@client.event
async def on_member_join(member):
    """Add new server users to the database while the bot is running.

    Parameters:
        member (discord.member.Member): Information about the user who joined the server
    """
    if member.bot:
        add_data_to_database(0, 'bots', 'bots_id', member.id)
    else:
        add_data_to_database(0, 'users', 'users_id', member.id)


@client.event
async def on_message(message):
    """Check for message and execute the function if the conditions are met.

    **Noteworthy:** If a bot receives a message from another bot or from itself, or does
    not receive the required command from the user, it does nothing

    Parameters:
        message (discord.message.Message): User message to perform required functions
    """
    if message.author == client.user or message.author.id in BLOCKED:
        return

    full_message = message.content.split(' ')
    args = message.content.split(' ')
    command = args.pop(0).lower()
    if command in ('ху', 'who'):
        await get_random_word(message, args)
    elif command == 'йа':
        await send_me_message(message, args)
    elif command == 'шип':
        await ship_func_chooser(message, args)
    elif command == 'хелп':
        await send_help_message(message)
    elif command == 'рандом':
        await get_random_number(message, args)
    elif command == 'макар':
        await send_ded_makar_message(message, args)
    elif command == 'рулетка':
        await start_roulette(message, args)
    elif command == 'uptime':
        await get_uptime_message(message)
    elif command == '!система' and message.author.id in ADMINS:
        await get_system_info(message)
    else:
        if 'тест' in full_message and full_message.index('тест') != 0 or \
           'рандом' in full_message and full_message.index('рандом') != 0:
            await who_is_user(message, full_message)


client.run(TOKENS[int(SELECTED_BOT)])
