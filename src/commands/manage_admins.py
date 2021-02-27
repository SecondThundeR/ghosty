"""Script for managing admin list of bot.

This script handles addition/removal id's of user to/from admin list

This file can also be imported as a module and contains the following functions:
    * admin_manager - checks if user is admin and executes required function
"""


from discord import channel
import asyncio
from src.libs.database_handler import is_data_in_database
from src.libs.database_handler import get_data_from_database
from src.libs.database_handler import add_data_to_database
from src.libs.database_handler import remove_data_from_database
from src.libs.user_handler import is_user_admin


async def admin_manager(bot, msg, args):
    """Check if user is admin and execute required operation.

    This function handles user checking and executing addition/deletion
    of user's ID to/from admin list

    Parameters:
        bot (discord.client.Client): Execute wait_for for waiting user's message
        msg (discord.message.Message): Execute send to channel function
        args (list): List with operation and user's ID
    """
    if (isinstance(msg.channel, channel.DMChannel)
            and len(args) == 2 and is_user_admin(msg)):
        if args[0] == 'добавить':
            await _add_admin(msg, args[1])
        elif args[0] == 'удалить':
            await _remove_admin(bot, msg, args[1])


async def _add_admin(msg, admin_id):
    """Add user's ID to admin list.

    This function handles addition of user's ID to admin list.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        admin_id (str): Admin's ID to add to list
    """
    if is_data_in_database(0, 'admin_list', 'admins_id', admin_id):
        await msg.channel.send('Данный пользователь уже админ')
    else:
        add_data_to_database(0, 'admin_list', 'admins_id', admin_id)
        await msg.channel.send('Я успешно добавил такого админа')


async def _remove_admin(bot, msg, admin_id):
    """Remove user's ID from admin list.

    This function handles removal of user's ID from admin list.

    **Noteworthy:** Since this list is very important for the bot's operation,
    several checks have been added here: if the list consists of one ID,
    it cancels the deletion, if the admin wants to delete himself,
    he is asked to confirm the action

    Parameters:
        bot (discord.client.Client): Execute wait_for for waiting user's message
        msg (discord.message.Message): Execute send to channel function
        admin_id (str): Admin's ID to remove from list
    """
    if msg.author.id == int(admin_id) and is_data_in_database(
        0,
        'admin_list',
        'admins_id',
        admin_id
    ):
        if len(get_data_from_database(0, 'admin_list', 'admins_id')) == 1:
            await msg.channel.send('Вы единственный админ бота. '
                                   'Управление ботом будет затруднено, '
                                   'если список админов будет пуст, '
                                   'поэтому я отменяю удаление')
        else:
            await msg.channel.send('Вы уверены что хотите убрать себя из списка?'
                                   ' (Да/Нет)')
            try:
                wait_msg = await bot.wait_for('message', timeout=15)
            except asyncio.TimeoutError:
                await msg.channel.send('Похоже вы не решились с выбором, '
                                       'пока что я отменил удаление вас из списка')
            else:
                if wait_msg.content.lower() == 'да':
                    remove_data_from_database(0, 'admin_list', 'admins_id', admin_id)
                    await msg.channel.send('Я удалил вас из админов :(')
                elif wait_msg.content.lower() in ['не', 'нет']:
                    await msg.channel.send('Удаление было отменено')
                else:
                    await msg.channel.send('Вы ответили как-то иначе, '
                                           'удаление было отменено')
    else:
        if not is_data_in_database(0, 'admin_list', 'admins_id', admin_id):
            await msg.channel.send('Данный пользователь не является админом')
        else:
            remove_data_from_database(0, 'admin_list', 'admins_id', admin_id)
            await msg.channel.send('Я успешно удалил такого админа')
