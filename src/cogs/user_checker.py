"""Get random percent of who the user is.

Also this script checks for two modes (test or random mode)

This file can also be imported as a module and contains the following functions:
    * who_is_user - sends random percent of who the user is
"""


from random import randint
from src.lib.exceptions import UsersNotFound
from src.lib.users import get_random_user


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
    random_percent = randint(0, 100)
    index_to_check = len(full_message) - 1
    test_data = _get_who_is_user(full_message)
    current_user = ''
    if 'тест' in full_message:
        if full_message.index('тест') == index_to_check:
            current_user = msg.author.mention
        else:
            current_user = full_message[index_to_check]
    if 'рандом' in full_message and 'тест' not in full_message:
        try:
            r_user = await get_random_user(msg)
        except UsersNotFound as warning:
            await msg.channel.send(f'Произошла ошибка: {warning}!')
            return
        current_user = r_user.mention
    if random_percent == 0:
        await msg.channel.send(f'{current_user} сегодня не {test_data} :c')
    elif random_percent == 100:
        await msg.channel.send(f'{current_user} кто бы мог подумать то! '
                               f'Ты {test_data} на {random_percent}%')
    else:
        await msg.channel.send(f'{current_user} {test_data} '
                               f'на {random_percent}%')
