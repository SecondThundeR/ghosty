"""Ship randomly selected users.

This script allows user to ship two random people or two chosen by user.
Script returns halves of each name and adds a heart.

This file can also be imported as a module and contains the following functions:
    * ship_func_chooser - choose correct function depending on statement
"""

from emoji import emoji_count
from asyncio import sleep
from datetime import datetime, timedelta
from src.lib.database import get_data, modify_data
from src.lib.exceptions import UsersNotFound
from src.lib.users import get_shipping_users, get_members_name


DELAY_TIME = 2
DELETE_TIME = 5


async def ship_func_chooser(msg, args):
    """Select correct function depending of statement.

    This function chooses another function to run, when
    certain statement is true

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments
    """
    if get_data(0, True, 'SELECT ship_in_active FROM variables') == 1:
        pass
    else:
        if args:
            if 'скип' in args:
                await _reset_ship(msg)
            elif 'фаст' in args:
                await _random_ship(msg, 'fast')
            else:
                await msg.channel.send(f'{msg.author.mention}, '
                                       'я не могу шипперить одного человека. '
                                       'Добавьте ещё кого-то, чтобы я смог '
                                       'сделать "магию"')
        elif len(args) == 2:
            await _custom_ship(msg, args)
        else:
            await _random_ship(msg)


async def _get_user_info(msg, user):
    """Get names of users from arguments.

    This function gets username if user provided mention of someone,
    otherwise return argument without changes

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        user (str): Custom names for shipping

    Returns:
        list: List with username and it's length divided by two
    """
    if user.startswith('<@!'):
        user_id = user[3:len(user) - 1]
        custom_member = await msg.guild.fetch_member(user_id)
        user_name = get_members_name(custom_member)
        user_length = int(len(user_name) / 2)
    else:
        user_name = user
        user_length = int(len(user_name) / 2)
    return [user_name, user_length]


async def _reset_ship(msg):
    """Reset latest ship results to start over.

    This function resets results of shipping to allow user execute
    new ship function

    Parameters:
        msg (discord.message.Message): Execute send to channel function
    """
    modify_data(
        0,
        'UPDATE variables SET ship_date = ?, ship_text_short = ?, '
        'ship_text_full = ?, ship_activated = ?',
        '',
        '',
        '',
        0
    )
    await msg.channel.send('Результаты шиппинга сброшены! '
                           '*(Вы разлучили, возможно, великолепную парочку!)*',
                           delete_after=DELETE_TIME)
    await sleep(DELETE_TIME)
    await msg.delete()


async def _custom_ship(msg, args):
    """Ship with two custom names from user.

    This function runs ship with two custom names from arguments,
    rather ship with random users

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments (Custom names for ship)
    """
    if emoji_count(msg.content) > 0:
        await msg.channel.send(f'{msg.author.mention}, '
                               'какой блин шип смайлов...',
                               delete_after=DELETE_TIME)
        await sleep(DELETE_TIME)
        await msg.delete()
    elif args[0].startswith('<@&') or args[1].startswith('<@&'):
        await msg.channel.send(f'{msg.author.mention}, к сожалению, '
                               'я не могу обработать это',
                               delete_after=DELETE_TIME)
        await sleep(DELETE_TIME)
        await msg.delete()
    elif args[0].startswith('<:') or args[1].startswith('<:'):
        await msg.channel.send(f'{msg.author.mention}, '
                               'какой блин шип эмодзи...',
                               delete_after=DELETE_TIME)
        await sleep(DELETE_TIME)
        await msg.delete()
    elif ('@everyone' in args[0] or '@here' in args[0] or
            '@everyone' in args[1] or '@here' in args[1]):
        await msg.channel.send(f'{msg.author.mention}, '
                               'похоже вы пытаетесь всунуть сюда '
                               '`@here` или `@everyone`, зачем?',
                               delete_after=DELETE_TIME)
        await sleep(DELETE_TIME)
        await msg.delete()
    else:
        first_user_info = await _get_user_info(msg, args[0])
        second_user_info = await _get_user_info(msg, args[1])
        first_username_part = first_user_info[0][:first_user_info[1]]
        second_username_part = second_user_info[0][second_user_info[1]:]
        final_name = first_username_part + second_username_part
        await msg.channel.send(f'Данная парочка смело бы называлась - **{final_name}**')


async def _random_ship(msg, mode='default'):
    """Ship with two randomly chosen names.

    This function runs ship with random users,
    rather shipping two custom names from arguments

    Parameters:
        msg (discord.message.Message): Execute send to channel function
    """
    current_date = datetime.now().date()
    new_date = (datetime.now() + timedelta(days=1)).date()
    ship_date = get_data(0, True, 'SELECT ship_date FROM variables')
    if (get_data(0, True, 'SELECT ship_activated FROM variables') == 0 and
            get_data(0, True, 'SELECT ship_in_active FROM variables') == 0):
        modify_data(
            0,
            'UPDATE variables SET ship_in_active = ?, ship_activated = ?',
            1,
            1
        )
        try:
            users_info = await get_shipping_users(msg)
        except UsersNotFound as warning:
            modify_data(
                0,
                'UPDATE variables SET ship_in_active = ?, ship_activated = ?',
                0,
                0
            )
            await msg.channel.send(f'Произошла ошибка: {warning}!',
                                   delete_after=DELETE_TIME)
            await sleep(DELETE_TIME)
            await msg.delete()
            return
        first_username = get_members_name(users_info[0])
        first_user_length = int(len(first_username) / 2)
        second_username = get_members_name(users_info[1])
        second_user_length = int(len(second_username) / 2)
        first_sliced_username = first_username[:first_user_length]
        second_sliced_username = second_username[second_user_length:]
        final_username = first_sliced_username + second_sliced_username
        ship_text_short = f'{users_info[0].mention} + {users_info[1].mention}'
        ship_text_full = f'{first_username} + {second_username}, #' + final_username
        if mode == 'fast':
            await msg.channel.send(f'**Парочка дня на сегодня:** {ship_text_short} '
                                   ':two_hearts:')
        else:
            await _random_ship_messages(msg, ship_text_short)
        modify_data(
            0,
            'UPDATE variables SET ship_date = ?, ship_text_full = ?, '
            'ship_text_short = ?, ship_in_active = ?',
            new_date,
            ship_text_full,
            ship_text_short,
            0
        )
    elif get_data(0, True, 'SELECT ship_in_active FROM variables') == 1:
        pass
    elif (get_data(0, True, 'SELECT ship_activated FROM variables') == 1 and
            current_date < datetime.strptime(ship_date, '%Y-%m-%d').date()):
        ship_text_full = get_data(0, True, 'SELECT ship_text_full FROM variables')
        next_date = get_data(0, True, 'SELECT ship_date FROM variables')
        next_date_string = _get_date_string(
            datetime.strptime(next_date, '%Y-%m-%d').weekday()
        )
        await msg.channel.send(f'**Парочка дня на сегодня:** {ship_text_full} '
                               ':two_hearts: \n\n*Следующий шиппинг будет доступен '
                               f'{next_date_string}*')
    elif (get_data(0, True, 'SELECT ship_activated FROM variables') == 1 and
            current_date >= datetime.strptime(ship_date, '%Y-%m-%d').date()):
        modify_data(0, 'UPDATE variables SET ship_activated = ?', 0)
        await _random_ship(msg)
    else:
        pass


async def _random_ship_messages(msg, short_text):
    """Send pre-messages and result of shipping.

    This function ships three pre-messages and final message with
    result of shipping

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        short_text (str): Ship's short text
    """
    await msg.channel.send('*чтож...*')
    await sleep(DELAY_TIME)
    await msg.channel.send('**МОРЕ ВОЛНУЕТСЯ РАЗ**')
    await sleep(DELAY_TIME)
    await msg.channel.send('**МОРЕ ВОЛНУЕТСЯ ДВА**')
    await sleep(DELAY_TIME)
    await msg.channel.send('**МОРЕ ВОЛНУЕТСЯ ТРИ**')
    await sleep(DELAY_TIME)
    await msg.channel.send(f'**В ЛЮБОВНОЙ ПОЗЕ ЗАСТРЯЛИ ** {short_text} '
                           ':two_hearts:')


def _get_date_string(weekday):
    """Return string of date.

    This function get weekday of ship date and returns weekday as string

    Parameters:
        weekday(int): Ship's weekday

    Returns:
        str: Weekday as a string
    """
    weekday_string = ''
    if weekday == 0:
        weekday_string = 'в Понедельник'
    elif weekday == 1:
        weekday_string = 'во Вторник'
    elif weekday == 2:
        weekday_string = 'в Среду'
    elif weekday == 3:
        weekday_string = 'в Четверг'
    elif weekday == 4:
        weekday_string = 'в Пятницу'
    elif weekday == 5:
        weekday_string = 'в Субботу'
    elif weekday == 6:
        weekday_string = 'в Воскресенье'
    return weekday_string
