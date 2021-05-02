"""Main script of Ghosty.

This is a Discord bot script that runs on the Discord.py library and
allows you to execute functions using specific text commands

There is the starting point of the bot control, from where it begin its
work. Here you can change the entire logic of the bot and adjust it to
fit your needs
"""


import time
import aiocron
import asyncio
import discord
import src.lib.database as database
import src.lib.users as users
import src.utils.avatar_changer as avatar_changer
import src.utils.general_scripts as general_scripts
from discord.ext import commands


TOKENS = database.get_data(1, False, 'SELECT bot_token FROM tokens')
SELECTED_BOT = database.get_data(0, True, 'SELECT current_selected_bot FROM variables')
DELAY_TIME = 5
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@aiocron.crontab('0 */3 * * *')
async def update_avatar():
    """Update avatar picture automatically every 3 hours.

    This function also checkes and updates the avatar_cooldown value
    to prevent a sudden avatar change during cron update
    """
    avatar_data = avatar_changer.get_avatar_bytes()
    if isinstance(avatar_data, int):
        pass
    else:
        await client.user.edit(avatar=avatar_data)


@client.event
async def on_ready():
    """Execute necessary functions on bot launch."""
    database.reset_tables()
    await general_scripts.load_commands(client)
    await general_scripts.update_member_list(client)
    await client.change_presence(status=discord.Status.dnd)
    avatar_data = avatar_changer.get_avatar_bytes()
    if isinstance(avatar_data, int):
        pass
    else:
        await client.user.edit(avatar=avatar_data)
    database.modify_data(
        0,
        'UPDATE variables SET bot_uptime = ?',
        int(time.time())
    )
    print(f'Successfully logged in as {client.user}!')



@client.event
async def on_command_error(ctx, error):
    """Handle `CommandNotFound` exception and send message about it.

    This function catches certain exception and sends message to user
    that provided command isn't valid

    Parameters:
        ctx (commands.context.Context): Context object to work with
        error (commands.errors.CommandNotFound): Error class
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply('Данной команды не существует. '
                        'Попробуйте ввести что-то другое!',
                        delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await ctx.message.delete()
    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.reply('Данной команда доступна только в личных сообщениях.',
                        delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await ctx.message.delete()
    else:
        raise error


@client.event
async def on_member_join(member):
    """Add new server users to database while bot is running.

    Parameters:
        member (discord.member.Member): Information about the joined user
    """
    users.add_member_to_db(member)


@client.event
async def on_member_leave(member):
    """Remove left server users from database while bot is running.

    Parameters:
        member (discord.member.Member): Information about the left user
    """
    users.rem_member_from_db(member)


client.run(TOKENS[int(SELECTED_BOT)])
