"""Text version of roulette game.

This module handles game logic of russian roulette.

This file can also be imported as a module and contains the following functions:
    * start_roulette - starts game and returning result of it
"""


import random
import asyncio
from src.libs.database_handler import get_data_from_database


DELAY_TIME = 3


def _get_random_word(condition):
    """Get random word from database.

    This function handles getting random word from DB
    depending on condition of game

    Parameters:
        condition (str): Condition of game when executed

    Returns:
        str: Random chosen word depending on condition
    """
    random_word = ''
    if condition == 'win':
        win_words_list = get_data_from_database(2, 'roulette_win_words', 'words')
        random_word = random.choice(win_words_list)
    if condition == 'lose':
        lose_words_list = get_data_from_database(2, 'roulette_lose_words', 'words')
        random_word = random.choice(lose_words_list)
    if condition == 'zero':
        zero_words_list = get_data_from_database(2, 'roulette_zero_words', 'words')
        random_word = random.choice(zero_words_list)
    if condition == 'minus':
        minus_words_list = get_data_from_database(2, 'roulette_minus_words', 'words')
        random_word = random.choice(minus_words_list)
    return random_word


async def start_roulette(msg, args):
    """Handle game logic and start game.

    This function handles all russian roulette logic.
    Also, it has certain checks for any non-standard situation

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments (Bullet count number)
    """
    bullet_list = []
    player = msg.author.mention
    deadly_bullet = 0
    bullet_count = 0

    if args == []:
        bullet_count = 1
    else:
        try:
            bullet_count = int(args[0])
        except ValueError:
            await msg.channel.send(f'{player}, похоже вы передали мне не число.'
                                   '\nПопробуйте ещё раз, '
                                   'но уже с правильными данными')

    if bullet_count == 0:
        await msg.channel.send(f'{player}, {_get_random_word("zero")}')
    elif bullet_count < 0:
        await msg.channel.send(f'{player}, {_get_random_word("minus")}')
    elif bullet_count == 6:
        await msg.channel.send('поздравляем! '
                               'теперь у нас на одного суицидника меньше. '
                               f'им был {player}!!!')
    elif bullet_count > 6:
        await msg.channel.send(f'{player}, если вдруг ты не знаешь, то напомню!'
                               '\nПо правилам русской рулетки, '
                               'можно брать только до 6 патронов')
    else:
        for i in range(bullet_count):
            charged_section_number = random.randint(1, 6)
            if charged_section_number in bullet_count:
                i -= 1
            else:
                bullet_list.append(charged_section_number)
        deadly_bullet = random.randint(1, 6)
        if deadly_bullet in bullet_list:
            await msg.channel.send('**БАХ**')
            await asyncio.sleep(DELAY_TIME)
            await msg.edit(content=f'{player}, {_get_random_word("lose")}')
        else:
            await msg.channel.send('*тишина*')
            await asyncio.sleep(DELAY_TIME)
            await msg.edit(content=f'{player}, {_get_random_word("win")}')
