"""Script for getting random percent of who the user is.

Also this script checks for two modes (test or random mode)

This file can also be imported as a module and contains the following functions:
    * who_is_user - sends random percent of who the user is
"""


import random
from src.libs.user_handler import get_random_user


def _get_who_is_user(message):
    """Group message content array.

    Parameters:
        message (list): List of message contents

    Returns:
        test_msg: Something to check with
    """
    try:
        mode_index = message.index('тест')
    except ValueError:
        mode_index = message.index('рандом')
    test_msg = " ".join(message[0:mode_index])
    return test_msg


async def who_is_user(msg, full_message):
    """Get random percent of who the user.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        full_message (list): List of message contents
    """
    random_percent = random.randint(0, 100)
    last_item_index = len(full_message) - 1
    test_data = _get_who_is_user(full_message)
    current_user = ''
    if 'рандом' in full_message:
        r_user = await get_random_user(msg)
        if r_user is None:
            await msg.channel.send(
                f'{msg.author.mention}, похоже cписок пользователей пуст и '
                f'поэтому мне не кого упоминать'
                )
            return
        current_user = r_user.mention
    elif 'тест' in full_message and full_message.index('тест') == last_item_index:
        current_user = msg.author.mention
    elif 'тест' in full_message and full_message.index('тест') != last_item_index:
        current_user = full_message[last_item_index]
    if random_percent == 0:
        await msg.channel.send(f'{current_user} сегодня не {test_data} :c')
    elif random_percent == 100:
        await msg.channel.send(
            f'{current_user} кто бы мог подумать то! '
            f'Ты {test_data} на {random_percent}%'
            )
    else:
        await msg.channel.send(
            f'{current_user} {test_data} '
            f'на {random_percent}%'
            )
