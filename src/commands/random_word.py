"""Module for getting random word from list.

This script sends randomly chosen word from list
Also, especially for this command, checks for spam messages

This file can also be imported as a module and contains the following functions:
    * get_random_word - sends message with randomly chosen word
"""


import random
import asyncio
from src.libs import random_user, database_handler

WORDS_ARRAY = database_handler.get_data_from_database('words', ['words_array'])
DELAY_TIME = 3


async def get_random_word(msg, args):
    """Get random word from list and send it.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments *(Custom name or mode of function)*
    """
    if len(args) == 0:
        current_user = msg.author.mention
    elif args[0] == 'рандом':
        r_user = await random_user.get_random_user(msg)
        if r_user is None:
            await msg.channel.send(
                f'{msg.author.mention}, похоже я не получил список пользователей и '
                f'поэтому мне не кого упоминать'
            )
            return
        current_user = r_user.mention
    else:
        current_user = args[0]
    if len(WORDS_ARRAY) == 0:
        await msg.channel.send(
            f'{msg.author.mention}, я пока не знаю никаких слов, '
            f'однако вы можете добавить новые слова в мой словарь',
            delete_after=DELAY_TIME
        )
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
    elif _check_for_spam(msg):
        await msg.channel.send(
            f'{msg.author.mention} куда спамиш?',
            delete_after=DELAY_TIME
        )
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
    else:
        await msg.channel.send(f'{current_user} {random.choice(WORDS_ARRAY)}')


def _check_for_spam(msg):
    """Get random word from list and send it.

    Parameters:
        msg (discord.message.Message): User ID to compare with database

    Returns:
        True if user hit message in a row limit, False otherwise
    """
    current_status = database_handler.get_data_from_database(
        'variables',
        ['spammerID', 'spammerCount']
    )
    if current_status[0] == msg.author.id:
        if current_status[1] >= 3:
            database_handler.edit_data_in_database(
                'variables',
                'spammerCount',
                0
            )
            return True
        database_handler.edit_data_in_database(
            'variables',
            'spammerCount',
            current_status[1] + 1
        )
        return False
    database_handler.edit_data_in_database(
        'variables',
        ['spammerID', 'spammerCount'],
        [msg.author.id, 1]
    )
    return False
