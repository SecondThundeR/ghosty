"""Script for managing ignore list of bot.

This script handles addition/removal id's of user to/from ignore list

This file can also be imported as a module and contains the following functions:
    * ignored_manager - checks if user is admin and executes reqired function
"""


from src.libs.database_handler import is_data_in_database
from src.libs.database_handler import add_data_to_database
from src.libs.database_handler import remove_data_from_database


async def ignored_manager(msg, args):
    """Check if user is admin and execute reqired operation.

    This function handles user checking and executing addition/deletion
    of user's ID to/from ignore list

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List with operation and user's ID
    """
    if len(args) == 2 and is_data_in_database(
        0,
        'admin_list',
        'admins_id',
        msg.author.id
    ):
        if args[0] == 'добавить':
            await _add_ignored(msg, args[1])
        elif args[0] == 'удалить':
            await _remove_ignored(msg, args[1])


async def _add_ignored(msg, block_id):
    """Add user's ID to ignore list.

    This function handles addition of user's ID to ignore list

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        block_id (str): ID of user to block
    """
    if is_data_in_database(0, 'admin_list', 'admins_id', block_id):
        await msg.channel.send('Я не могу заблокировать админа...')
    else:
        if is_data_in_database(0, 'block_list', 'blocked_id', block_id):
            await msg.channel.send('Данный пользователь уже заблокирован')
        else:
            add_data_to_database(0, 'block_list', 'blocked_id', block_id)
            await msg.channel.send('Я успешно заблокировал этого юзера')


async def _remove_ignored(msg, block_id):
    """Remove user's ID from ignore list.

    This function handles removal of user's ID from ignore list

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        block_id (str): ID of user to unblock
    """
    if not is_data_in_database(0, 'block_list', 'blocked_id', block_id):
        await msg.channel.send('Данный юзер уже разблокирован')
    else:
        remove_data_from_database(0, 'block_list', 'blocked_id', block_id)
        await msg.channel.send('Я успешно разблокировал этого юзера')
