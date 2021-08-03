"""Entry point of Ghosty bot.

This is a bot script that runs on the Discord.py library and
allows you to execute functions using specific text commands

There is the starting point of the bot control, from where it begin its
work. Here you can change the entire logic of the bot and adjust it to
fit your needs
"""


import time
import aiocron
import discord
import src.lib.database as database
import src.lib.users as users
import src.utils.avatar_changer as avatar_changer
import src.utils.general_scripts as general_scripts
import src.utils.markov_utils as markov_utils
from discord.ext import commands


TOKENS = database.get_data(
    'confDB',
    False,
    'SELECT bot_token FROM tokens'
)
SELECTED_BOT = database.get_data(
    'mainDB',
    True,
    'SELECT current_selected_bot FROM variables'
)
DELAY_TIME = 3
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@aiocron.crontab('0 */3 * * *')
async def update_avatar():
    """Update avatar picture periodically.

    This function changes the bot avatar every 3 hours using a cron job.
    It also checks and updates the `avatar_cooldown` value
    to lock manual avatar changing during/after updating by cron job,
    which helps prevent getting a cooldown from the Discord API.
    """
    avatar_data = avatar_changer.get_avatar_bytes()
    if avatar_data['avatar_bytes']:
        await client.user.edit(avatar=avatar_data['avatar_bytes'])


@client.event
async def on_ready():
    """Execute necessary functions.

    This function executes certain actions on bot's load, such as:
        - Resetting DB table and delay of randomly generated Markov message
        - Loading commands
        - Updating table with users
        - Changing bot's status and avatar
        - Setting up new bot's uptime
    """
    database.clear_tables()
    markov_utils.markov_delay_handler('clear')
    await client.change_presence(status=discord.Status.dnd)
    avatar_data = avatar_changer.get_avatar_bytes()
    if avatar_data['avatar_bytes']:
        await client.user.edit(avatar=avatar_data['avatar_bytes'])
    await general_scripts.load_commands(client)
    await general_scripts.update_member_list(client)
    database.modify_data(
        'mainDB',
        'UPDATE variables SET bot_uptime = ?',
        int(time.time())
    )
    print(f'Successfully logged in as {client.user}!')


@client.event
async def on_command_error(ctx, error):
    """Handle commands exceptions.

    This function catches certain exception and sends info message to the user
    Currently, this commands handles `CommandNotFound` and `PrivateMessageOnly`

    Args:
        ctx (discord.ext.commands.Context): The invocation context
        error (discord.ext.commands.CommandError): The error that was raised

    Raises:
        discord.ext.commands.CommandError: It there is an error
        that isn't included in the handling
    """
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.reply('Данной команда доступна только в личных сообщениях.',
                        delete_after=DELAY_TIME)
    else:
        raise error


@client.event
async def on_member_join(member):
    """Add new server users to database.

    This function adds every new user/bot to database, while bot is running.
    This helps prevent new users from being ignored in commands
    that use use a table of users (And helps to ignore any bot in commands)

    Args:
        member (discord.member.Member): Data about joined user/bot
    """
    if not member.bot:
        users.add_member_to_db(member.id)
        return
    users.add_bot_to_db(member.id)


@client.event
async def on_member_leave(member):
    """Remove left server users from database.

    This function removes every left user from database, while bot is running.
    This helps to prevent any problems with commands that use a table of users.

    Args:
        member (discord.member.Member): Data about left user
    """
    if not member.bot:
        users.rem_member_from_db(member.id)


@client.listen('on_message')
async def get_messages(message):
    """Listener for regular messages (Non-commands).

    This function is used to receive all regular messages used for Markov chains.

    Args:
        message (discord.message.Message): User message to perform required functions
    """
    if not message.author.bot:
        message_body = message.content
        msg_check = markov_utils.check_message_content(message_body)
        if not msg_check:
            return
        words = message_body.split()
        counter_list = markov_utils.markov_delay_handler('get')
        if counter_list[0] <= counter_list[1]:
            new_sentence = markov_utils.return_checked_sentence()
            if new_sentence:
                await message.channel.send(new_sentence)
            markov_utils.markov_delay_handler('clear')
        else:
            markov_utils.message_words_to_db(words)
            markov_utils.markov_delay_handler('update')


client.run(TOKENS[int(SELECTED_BOT)])
