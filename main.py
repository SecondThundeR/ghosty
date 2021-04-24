"""secondthunder-py-bot.

This is a Discord bot script that runs on the Discord.py library and
allows you to execute functions using specific text commands

There is the starting point of the bot control, from where it begin its
work. Here you can change the entire logic of the bot and adjust it to
fit your needs
"""


from aiocron import crontab
from time import time as curr_time
from discord import Client, Intents, Status
from src.lib.database import clear_on_load, get_data, modify_data
from src.lib.users import add_member_to_db
from src.cogs.help import send_help_message
from src.cogs.makar import send_makar_message
from src.cogs.manage_admins import admin_manager
from src.cogs.manage_ignored import ignored_manager
from src.cogs.me import send_me_message
from src.cogs.poll import init_poll
from src.cogs.random_number import get_random_number
from src.cogs.random_ship import ship_func_chooser
from src.cogs.random_word import get_random_word
from src.cogs.rsp import rsp_mode
from src.cogs.russian_roulette import start_roulette
from src.cogs.switch_avatar import switch_avatar
from src.cogs.system import get_system_info
from src.cogs.uptime import get_bot_uptime
from src.cogs.user_checker import who_is_user
from src.cogs.user_finder import user_finder_mode
from src.utils.avatar_changer import get_avatar_bytes


TOKENS = get_data(1, False, 'SELECT bot_token FROM tokens')
SELECTED_BOT = get_data(0, True, 'SELECT current_selected_bot FROM variables')
intents = Intents.default()
intents.members = True
client = Client(intents=intents)


@crontab('0 */6 * * *')
async def update_avatar():
    """Update avatar picture automatically every 6 hours.
    
    This function also checkes and updates the avatar_cooldown value
    to prevent a sudden avatar change during cron update
    """
    avatar_data = get_avatar_bytes()
    if isinstance(avatar_data, int):
        pass
    else:
        await client.user.edit(avatar=avatar_data)


@client.event
async def on_ready():
    """Execute necessary functions during the bot launch."""
    clear_on_load()
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            add_member_to_db(member.id)
    await client.change_presence(status=Status.dnd)
    avatar_data = get_avatar_bytes()
    if isinstance(avatar_data, int):
        pass
    else:
        await client.user.edit(avatar=avatar_data)
    print(f'Successfully logged in as {client.user}!')
    modify_data(0, 'UPDATE variables SET bot_uptime = ?', int(curr_time()))


@client.event
async def on_member_join(member):
    """Add new server users to the database while the bot is running.

    Parameters:
        member (discord.member.Member): Information about the user who joined the server
    """
    add_member_to_db(member.id)


@client.event
async def on_message(message):
    """Check for message and execute the function if the conditions are met.

    **Noteworthy:** If a bot receives a message from another bot or from itself, or does
    not receive the required command from the user, it does nothing

    Parameters:
        message (discord.message.Message): User message to perform required functions
    """
    if message.author == client.user or message.author.id in get_data(
        0,
        False,
        'SELECT blocked_id FROM block_list'
    ):
        return

    full_message = message.content.split(' ')
    args = message.content.split(' ')
    command = args.pop(0).lower()

    if command == 'полл':
        await init_poll(message, args)
    elif command == 'макар':
        await send_makar_message(message, args)
    elif command == 'хелп':
        await send_help_message(message)
    elif command == 'uptime':
        await get_bot_uptime(message)
    elif command in 'админ':
        await admin_manager(client, message, args)
    elif command in 'чс':
        await ignored_manager(message, args)
    elif command == 'йа':
        await send_me_message(message, args)
    elif command == 'рандом':
        await get_random_number(message, args)
    elif command == 'шип':
        await ship_func_chooser(message, args)
    elif command == 'цуефа':
        await rsp_mode(client, message, args)
    elif command == 'рулетка':
        await start_roulette(message, args)
    elif command == 'аватарка':
        await switch_avatar(message, client)
    elif command == 'система':
        await get_system_info(message)
    elif command in ('ху', 'who'):
        await get_random_word(message, args)
    elif command == 'поиск':
        await user_finder_mode(message, args)
    else:
        if ('тест' in full_message and full_message.index('тест') != 0
                or 'рандом' in full_message and full_message.index('рандом') != 0):
            await who_is_user(message, full_message)


client.run(TOKENS[int(SELECTED_BOT)])
