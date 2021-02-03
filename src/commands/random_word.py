"""Script for getting random word from list.

This script sends randomly chosen word from list
Also, especially for this command, checks for spam messages

This file can also be imported as a module and contains the following functions:
    * get_random_word - sends message with randomly chosen word
"""


import random
import asyncio
from src.libs.database_handler import get_data_from_database
from src.libs.database_handler import edit_data_in_database
from src.libs.user_handler import get_random_user
from src.libs.words_base_handler import add_word
from src.libs.words_base_handler import delete_word


WORDS_ARRAY = get_data_from_database(2, 'main_words_base', 'words')
DELAY_TIME = 3


async def get_random_word(msg, args):
    """Get random word from list and send it.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments (Custom name or mode of function)
    """
    current_user = None
    if len(args) == 0:
        current_user = msg.author.mention
    else:
        if args[0] == 'добавить':
            args.pop(0)
            word_to_add = "".join(args)
            await msg.channel.send(add_word(word_to_add), delete_after=DELAY_TIME)
            await asyncio.sleep(DELAY_TIME)
            await msg.delete()
            return

        if args[0] == 'удалить':
            args.pop(0)
            word_to_delete = "".join(args)
            await msg.channel.send(delete_word(word_to_delete), delete_after=DELAY_TIME)
            await asyncio.sleep(DELAY_TIME)
            await msg.delete()
            return

        if args[0] == 'рандом':
            r_user = await get_random_user(msg)
            if r_user is None:
                await msg.channel.send(f'{msg.author.mention}, '
                                       'похоже cписок пользователей пуст '
                                       'и поэтому мне не кого упоминать')
                return
            current_user = r_user.mention
        else:
            current_user = args[0]

    if len(WORDS_ARRAY) == 0:
        await msg.channel.send(f'{msg.author.mention}, я пока не знаю никаких слов, '
                               'однако вы можете добавить новые слова в мой словарь',
                               delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
    elif _check_for_spam(msg):
        await msg.channel.send(f'{msg.author.mention} куда спамиш?',
                               delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
    else:
        await msg.channel.send(f'{current_user} {random.choice(WORDS_ARRAY)}')


def _check_for_spam(msg):
    """Get random word from list and send it.

    Parameters:
        msg (discord.message.Message): User ID to compare with database

    Returns:
        bool: True if user hit message in a row limit, False otherwise
    """
    current_status = get_data_from_database(
        0,
        'variables',
        ['spammer_ID', 'spammer_count']
    )
    if current_status[0] == msg.author.id:
        if current_status[1] >= 3:
            edit_data_in_database(
                0,
                'variables',
                'spammer_count',
                0
            )
            return True
        edit_data_in_database(
            0,
            'variables',
            'spammer_count',
            current_status[1] + 1
        )
        return False
    edit_data_in_database(
        0,
        'variables',
        ['spammer_ID', 'spammer_count'],
        [msg.author.id, 1]
    )
    return False
