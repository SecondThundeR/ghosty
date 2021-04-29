"""Search *insert any word or something else here*.

This script repeats the good old meme about search *p-word*

This file can also be imported as a module and contains the following functions:
    * user_finder_mode - executes required finder mode depending on arguments
"""


from asyncio import sleep
from src.lib.exceptions import UsersNotFound
from src.lib.users import get_random_user


DELAY_TIME = 2


async def user_finder_mode(msg, args):
    """Execute required finder mode depending on arguments.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List with required mode of finder
    """
    if not args:
        pass
    else:
        if args[0] == 'пидорасов':
            await _pidor_finder(msg)


async def _pidor_finder(msg):
    """Get random user and launch 'finder' of *p-word*.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
    """
    try:
        r_user = await get_random_user(msg)
    except UsersNotFound as warning:
        await msg.channel.send(f'Произошла ошибка: {warning}!')
        return
    await msg.channel.send('Система поиска пидорасов активирована!')
    await sleep(DELAY_TIME)
    await msg.channel.send('*пип*')
    await sleep(DELAY_TIME)
    await msg.channel.send('*пип*')
    await sleep(DELAY_TIME)
    await msg.channel.send('*пип*')
    await sleep(DELAY_TIME)
    await msg.channel.send(f'Пидорас найден ({r_user.mention})')
