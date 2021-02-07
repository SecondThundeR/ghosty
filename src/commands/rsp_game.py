"""Text version of RSP game.

This script handles game logic of rock scissors paper.

This file can also be imported as a module and contains the following functions:
    * rsp_mode - starts game with bot/users
"""


import discord
import random
import asyncio
from src.libs.database_handler import edit_data_in_database
from src.libs.database_handler import get_data_from_database


FAIL_DELAY = 4
SUCCESS_DELAY = 1
rsp_win_variants = {
  'камень': 'ножницы',
  'бумага': 'камень',
  'ножницы': 'бумага'
}


async def rsp_mode(bot, msg, args):
    """Execute correct mode of game depending on arguments.

    If arguments aren't provided, executes multiplayer game.
    Otherwise, executes game with bot

    Parameters:
        bot (discord.client.Client): Execute wait_for for waiting user's message
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments (RSP variants, if playing with bot)
    """
    if not args:
        if get_data_from_database(0, 'variables', 'rsp_game_active')[0] == 1:
            await msg.channel.send('Сессия игры уже запущена, '
                                   'чтобы начать новую игру, закончите старую')
        else:
            await _rsp_multi_game(bot, msg)
            return
    else:
        await _rsp_bot_game(bot, msg, args[0])


def _join_check(msg):
    """Check for correct command to join.

    Parameters:
        msg (discord.message.Message): Get content from message and author's ID

    Returns:
        True, if all conditions are met
    """
    if (msg.content.lower() == 'играть'
            and not isinstance(msg.channel, discord.channel.DMChannel)):
        return True
    return False


def _choice_check(msg):
    """Check for correct answer from user.

    Parameters:
        msg (discord.message.Message): Get content from message

    Returns:
        True, if all conditions are met
    """
    if (msg.content.lower() in rsp_win_variants
            and isinstance(msg.channel, discord.channel.DMChannel)):
        return True
    return False


async def _purge_messages(messages):
    """Delete all messages, that can distract users in channel.

    Parameters:
        message (list): List with messages to delete
    """
    msg_counter = 0
    for i, message in enumerate(messages):
        await message.delete()
        msg_counter += 1
    print(f'[RSP Game] Deleted {i} messages')



def _rsp_game_logic(first_var, second_var, first_user_id, second_user_id):
    """Get the outcome of the game and return its result.

    This function handles check for winner of RSP
    If no one wins, throw 'Draw'

    Parameters:
        first_var (str): First player choice
        second_var (str): Second player choice
        first_user_id (int): First player ID to mention
        second_user_id (int): Second player ID to mention

    Returns:
        str: Outcome of the game
    """
    f_user_mention = f'<@{first_user_id}>'
    s_user_mention = f'<@{second_user_id}>'
    end_text = '**Игра между ' \
               f'{f_user_mention} и {s_user_mention} ' \
               'окончена!**\n'
    outcome_text = ''
    if first_var == rsp_win_variants[second_var]:
        outcome_text = f'**Результаты:** {second_var}  🤜  {first_var}\n' \
                       f'{s_user_mention} победил!'
    elif second_var == rsp_win_variants[first_var]:
        outcome_text = f'**Результаты:** {first_var}  🤜  {second_var}\n' \
                       f'{f_user_mention} победил!'
    else:
        outcome_text = f'**Результаты:** {first_var}  🙏  {second_var}\n' \
                       'И у нас ничья!'
    return end_text + outcome_text


async def _rsp_bot_game(bot, msg, user_choice):
    """Game with bot.

    This function executes random choice of bot and comparing it with
    players choice

    Parameters:
        bot (discord.client.Client): Get current bot ID
        msg (discord.message.Message): Execute send to channel function
        user_choice (str): Player's move variant
    """
    if user_choice not in rsp_win_variants:
        await msg.channel.send(f'{msg.author.mention}, '
                               'похоже вы выбрали что-то не то...')
    else:
        bot_choice = random.choice(list(rsp_win_variants))
        await msg.channel.send(_rsp_game_logic(user_choice, bot_choice,
                                               msg.author.id, bot.user.id))


async def _rsp_multi_game(bot, msg):
    """Game with other users of server.

    This function executes game with other users.

    Also, it waits for another user to play,
    and waits for a response from each in turn,
    then displays the outcome of the game

    **Noteworthy:** When game is live, lock other games to be played,
    while current game isn't finished

    Parameters:
        bot (discord.client.Client): Execute wait_for for waiting user's message
        msg (discord.message.Message): Execute send to channel function
    """
    edit_data_in_database(0, 'variables', 'rsp_game_active', 1)
    current_channel = msg.channel
    first_user = msg.author
    users_choice = []
    messages_to_purge = []
    await msg.delete()
    init_msg = await current_channel.send(f'{first_user.mention} запустил игру! '
                                          'Второй игрок, напишите "Играть"\n'
                                          '*Время ожидания второго игрока - 1 минута*')
    messages_to_purge.append(init_msg)
    try:
        s_user_wait = await bot.wait_for('message', timeout=60, check=_join_check)
        second_user = s_user_wait.author
    except asyncio.TimeoutError:
        edit_data_in_database(0, 'variables', 'rsp_game_active', 0)
        game_fail = current_channel.send(f'{first_user.mention}, '
                                         'похоже никто не решил сыграть с вами. '
                                         'Пока что я отменил данную игру')
        messages_to_purge.append(game_fail)
        await asyncio.sleep(FAIL_DELAY)
        await _purge_messages(messages_to_purge)
        return
    else:
        if s_user_wait.author.id == first_user.id:
            edit_data_in_database(0, 'variables', 'rsp_game_active', 0)
            f_user_join = await current_channel.send(f'{first_user.mention}, '
                                                     'решил поиграть сам собой, '
                                                     'отменяю данную игру')
            messages_to_purge.append(s_user_wait)
            messages_to_purge.append(f_user_join)
            await asyncio.sleep(FAIL_DELAY)
            await _purge_messages(messages_to_purge)
            return
    await s_user_wait.delete()
    await init_msg.edit(content='Сейчас идёт игра между '
                                f'{first_user.mention} и {second_user.mention}')
    try:
        await first_user.send('Ваш вариант *(На ответ 1 минута)*:')
        first_response = await bot.wait_for('message', timeout=30, check=_choice_check)
        users_choice.append(first_response.content.lower())
    except asyncio.TimeoutError:
        edit_data_in_database(0, 'variables', 'rsp_game_active', 0)
        f_move_fail = await current_channel.send(f'{first_user.mention} '
                                                 'не успел отправить вариант вовремя. '
                                                 'Игра отменена')
        messages_to_purge.append(f_move_fail)
        await asyncio.sleep(FAIL_DELAY)
        await _purge_messages(messages_to_purge)
        return
    try:
        await second_user.send('Ваш вариант *(На ответ 1 минута)*:')
        second_response = await bot.wait_for('message', timeout=30, check=_choice_check)
        users_choice.append(second_response.content.lower())
    except asyncio.TimeoutError:
        edit_data_in_database(0, 'variables', 'rsp_game_active', 0)
        s_move_fail = await current_channel.send(f'{second_user.mention} '
                                                 'не успел отправить вариант вовремя. '
                                                 'Игра отменена')
        messages_to_purge.append(s_move_fail)
        await asyncio.sleep(FAIL_DELAY)
        await _purge_messages(messages_to_purge)
        return
    edit_data_in_database(0, 'variables', 'rsp_game_active', 0)
    await current_channel.send(_rsp_game_logic(users_choice[0], users_choice[1],
                                               first_user.id, second_user.id))
    await _purge_messages(messages_to_purge)
