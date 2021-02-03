"""Text version of roulette game.

This script handles game logic of russian roulette.

This file can also be imported as a module and contains the following functions:
    * start_roulette - starts game and returning result of it
"""


import random
import asyncio
from src.libs.database_handler import get_data_from_database
from src.libs.words_base_handler import add_roulette_word
from src.libs.words_base_handler import delete_roulette_word


TABLES_ALIASES = {
    'вин': 'win',
    'луз': 'lose',
    'ноль': 'zero',
    'минус': 'minus'}
ADMIN_LIST = get_data_from_database(0, 'admin_list', 'admins_id')
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
        WIN_WORDS_LIST = get_data_from_database(2, 'roulette_win_words', 'words')
        random_word = random.choice(WIN_WORDS_LIST)
    if condition == 'lose':
        LOSE_WORDS_LIST = get_data_from_database(2, 'roulette_lose_words', 'words')
        random_word = random.choice(LOSE_WORDS_LIST)
    if condition == 'zero':
        ZERO_WORDS_LIST = get_data_from_database(2, 'roulette_zero_words', 'words')
        random_word = random.choice(ZERO_WORDS_LIST)
    if condition == 'minus':
        MINUS_WORDS_LIST = get_data_from_database(2, 'roulette_minus_words', 'words')
        random_word = random.choice(MINUS_WORDS_LIST)
    return random_word


async def start_roulette(msg, args):
    """Handle game logic and start game.

    This function handles all russian roulette logic.
    Also, it has certain checks for any non-standard situation

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments (Bullet count number)
    """
    PLAYER = msg.author.mention
    bullet_list = []
    deadly_bullet = 0
    bullet_count = 0

    if args == []:
        bullet_count = 1
    else:
        if args[0] == 'добавить':
            if args[1] in TABLES_ALIASES:
                TABLE_TO_MODIFY = TABLES_ALIASES[args[1]]
                for i in range(2):
                    args.pop(0)
                WORD_TO_ADD = " ".join(args)
                await msg.channel.send(add_roulette_word(WORD_TO_ADD, TABLE_TO_MODIFY),
                                       delete_after=DELAY_TIME)
                await asyncio.sleep(DELAY_TIME)
                await msg.delete()
            return
        if args[0] == 'удалить':
            if msg.author.id in ADMIN_LIST and args[1] in TABLES_ALIASES:
                TABLE_TO_MODIFY = TABLES_ALIASES[args[1]]
                for i in range(2):
                    args.pop(0)
                WORD_TO_DELETE = " ".join(args)
                await msg.channel.send(delete_roulette_word(
                                       WORD_TO_DELETE, TABLE_TO_MODIFY
                                       ),
                                       delete_after=DELAY_TIME)
                await asyncio.sleep(DELAY_TIME)
                await msg.delete()
            return

        try:
            bullet_count = int(args[0])
        except ValueError:
            await msg.channel.send(f'{PLAYER}, похоже вы передали мне не число.'
                                   '\nПопробуйте ещё раз, '
                                   'но уже с правильными данными')
            return

    if bullet_count == 0:
        await msg.channel.send(f'{PLAYER}, {_get_random_word("zero")}')
    elif bullet_count < 0:
        await msg.channel.send(f'{PLAYER}, {_get_random_word("minus")}')
    elif bullet_count == 6:
        await msg.channel.send('поздравляем! '
                               'теперь у нас на одного суицидника меньше. '
                               f'им был {PLAYER}!!!')
    elif bullet_count > 6:
        await msg.channel.send(f'{PLAYER}, если вдруг ты не знаешь, то напомню!'
                               '\nПо правилам русской рулетки, '
                               'можно брать только до 6 патронов')
    else:
        for i in range(bullet_count):
            CHARGED_SECTION = random.randint(1, 6)
            if CHARGED_SECTION in bullet_list:
                i -= 1
            else:
                bullet_list.append(CHARGED_SECTION)
        deadly_bullet = random.randint(1, 6)
        if deadly_bullet in bullet_list:
            bot_message = await msg.channel.send('**БАХ**')
            await asyncio.sleep(DELAY_TIME)
            await bot_message.edit(content=f'{PLAYER}, {_get_random_word("lose")}')
        else:
            bot_message = await msg.channel.send('*тишина*')
            await asyncio.sleep(DELAY_TIME)
            await bot_message.edit(content=f'{PLAYER}, {_get_random_word("win")}')
