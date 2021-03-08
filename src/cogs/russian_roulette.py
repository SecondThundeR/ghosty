"""Init text version of roulette game.

This script handles game logic of russian roulette.

This file can also be imported as a module and contains the following functions:
    * start_roulette - starts game and returning result of it
"""


from random import choice, randint
from asyncio import sleep
from src.lib.database import get_data
from src.lib.words_base import manage_r_word


TABLES_ALIASES = {
    'вин': 'win',
    'луз': 'lose',
    'ноль': 'zero',
    'минус': 'minus'}
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
    if condition == 'win':
        WIN_WORDS_LIST = get_data(2, False, 'SELECT words FROM roulette_win_words')
        random_word = choice(WIN_WORDS_LIST)
    if condition == 'lose':
        LOSE_WORDS_LIST = get_data(2, False, 'SELECT words FROM roulette_lose_words')
        random_word = choice(LOSE_WORDS_LIST)
    if condition == 'zero':
        ZERO_WORDS_LIST = get_data(2, False, 'SELECT words FROM roulette_zero_words')
        random_word = choice(ZERO_WORDS_LIST)
    if condition == 'minus':
        MINUS_WORDS_LIST = get_data(2, False, 'SELECT words FROM roulette_minus_words')
        random_word = choice(MINUS_WORDS_LIST)
    return random_word


async def start_roulette(msg, args):
    """Handle game logic and start game.

    This function handles all russian roulette logic.
    Also, it has certain checks for any non-standard situation

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments (Bullet count number)
    """
    class Roulette:

        """A class to represent a database.

        Parameters:
            player (discord.member.Member): Info about player to mention
        """

        def __init__(self, player):
            self.player = player.mention
            self.bullet_list = []
            self.bullet_count = 0

    roulette = Roulette(msg.author)

    if not args:
        roulette.bullet_count = 1
    else:
        if args[0] == 'добавить':
            if args[1] in TABLES_ALIASES:
                TABLE_TO_MODIFY = TABLES_ALIASES[args[1]]
                for i in range(2):
                    args.pop(0)
                WORD_TO_ADD = " ".join(args)
                await msg.channel.send(manage_r_word(
                                        WORD_TO_ADD,
                                        TABLE_TO_MODIFY,
                                        'add'
                                       ),
                                       delete_after=DELAY_TIME)
                await sleep(DELAY_TIME)
                await msg.delete()
            return
        if args[0] == 'удалить':
            if (get_data(
                    0,
                    True,
                    'SELECT * FROM admin_list '
                    'WHERE admins_id = ?',
                    msg.author.id
                ) and args[1] in TABLES_ALIASES
            ):
                TABLE_TO_MODIFY = TABLES_ALIASES[args[1]]
                for i in range(2):
                    args.pop(0)
                WORD_TO_DELETE = " ".join(args)
                await msg.channel.send(manage_r_word(
                                        WORD_TO_DELETE,
                                        TABLE_TO_MODIFY,
                                        'del'
                                       ),
                                       delete_after=DELAY_TIME)
                await sleep(DELAY_TIME)
                await msg.delete()
            return

        try:
            roulette.bullet_count = int(args[0])
        except ValueError:
            await msg.channel.send(f'{roulette.player}, похоже вы передали не число.'
                                   '\nПопробуйте ещё раз, '
                                   'но уже с правильными данными')
            return

    if roulette.bullet_count == 0:
        await msg.channel.send(f'{roulette.player}, {_get_random_word("zero")}')
    elif roulette.bullet_count < 0:
        await msg.channel.send(f'{roulette.player}, {_get_random_word("minus")}')
    elif roulette.bullet_count == 6:
        await msg.channel.send('поздравляем! '
                               'теперь у нас на одного суицидника меньше. '
                               f'им был {roulette.player}!!!')
    elif roulette.bullet_count > 6:
        await msg.channel.send(f'{roulette.player}, стоит напомнить, '
                               'что по правилам русской рулетки, '
                               'можно брать только до 6 патронов')
    else:
        for i in range(roulette.bullet_count):
            CHARGED_SECTION = randint(1, 6)
            if CHARGED_SECTION in roulette.bullet_list:
                i -= 1
            else:
                roulette.bullet_list.append(CHARGED_SECTION)
        deadly_bullet = randint(1, 6)
        if deadly_bullet in roulette.bullet_list:
            bot_message = await msg.channel.send('**БАХ**')
            await sleep(DELAY_TIME)
            await bot_message.edit(content=f'{roulette.player}, '
                                           f'{_get_random_word("lose")}')
        else:
            bot_message = await msg.channel.send('*тишина*')
            await sleep(DELAY_TIME)
            await bot_message.edit(content=f'{roulette.player}, '
                                           f'{_get_random_word("win")}')
