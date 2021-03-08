"""Manage ignore list of bot.

This script handles addition/removal id's of user to/from ignore list

This file can also be imported as a module and contains the following functions:
    * ignored_manager - checks if user is admin and executes required function
"""


from discord import channel
from src.lib.database import modify_data
from src.lib.users import is_user_admin, is_user_blocked


async def ignored_manager(msg, args):
    """Check if user is admin and execute required operation.

    This function handles user checking and executing addition/deletion
    of user's ID to/from ignore list

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List with operation and user's ID
    """
    if (isinstance(msg.channel, channel.DMChannel)
            and len(args) == 2 and is_user_admin(msg.author.id)):
        if args[0] == 'заблокировать':
            await _add_ignored(msg, args[1])
        elif args[0] == 'разблокировать':
            await _remove_ignored(msg, args[1])


async def _add_ignored(msg, user_id):
    """Add user's ID to blacklist.

    This function handles addition of user's ID to ignore list

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        user_id (int): User's ID to ban
    """
    if is_user_admin(user_id):
        await msg.channel.send('Я не могу заблокировать админа...')
    else:
        if is_user_blocked(user_id):
            await msg.channel.send('Данный пользователь уже заблокирован')
        else:
            modify_data(0, 'INSERT INTO block_list VALUES (?)', user_id)
            await msg.channel.send('Я успешно заблокировал этого юзера')


async def _remove_ignored(msg, user_id):
    """Remove user's ID from ignore list.

    This function handles removal of user's ID from ignore list

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        user_id (int): User's ID to unban
    """
    if not is_user_blocked(user_id):
        await msg.channel.send('Данный юзер уже разблокирован')
    else:
        modify_data(0, 'DELETE FROM block_list WHERE blocked_id = ?', user_id)
        await msg.channel.send('Я успешно разблокировал этого юзера')
