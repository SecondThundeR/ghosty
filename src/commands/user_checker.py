"""Module for getting random percent of who the user is.

Also this script checks for two modes (test or random mode)

This file can also be imported as a module and contains the following functions:
    * who_is_user - sends random percent of who the user is
"""


from random import randint
from src.libs.user_handler import get_random_user


def _group_message_contents(message):
    """Group message content array and return grouped list

    Parameters:
        message (list): List of message contents

    Returns:
        list: Grouped list of message contents
    """
    try:
        mode_index = message.index('тест')
        current_mode = message[mode_index]
    except ValueError:
        mode_index = message.index('рандом')
        current_mode = message[mode_index]
    test_msg = " ".join(message[0:mode_index])
    return [current_mode, test_msg]


async def who_is_user(msg, full_message):
    """Get random percent of who the user

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        fullMessage (list): List of message contents
    """
    random_percent = randint(0, 100)
    user_checker_data = _group_message_contents(full_message)
    current_user = ''
    if user_checker_data[0] == 'рандом':
        r_user = await get_random_user(msg)
        if r_user is None:
            await msg.channel.send(
                f'{msg.author.mention}, похоже cписок пользователей пуст и '
                f'поэтому мне не кого упоминать'
                )
            return
        current_user = r_user.mention
    elif user_checker_data[0] == 'тест':
        current_user = msg.author.mention
    if random_percent == 0:
        await msg.channel.send(f'{current_user} сегодня не {user_checker_data[1]} :c')
    elif random_percent == 100:
        await msg.channel.send(
        f'{current_user} кто бы мог подумать то! '
        f'Ты {user_checker_data[1]} на {random_percent}%')
    else:
        await msg.channel.send(f'{current_user} {user_checker_data[1]} на {random_percent}%')
