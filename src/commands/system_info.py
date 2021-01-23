"""Module for getting info about machine, where bot is running.

This file can also be imported as a module and contains the following functions:
    * get_system_info - retrives system info and sends it as message
"""


from platform import system
from platform import release
from platform import version
from platform import processor
from platform import machine
from asyncio import sleep

DELAY_TIME = 5


async def get_system_info(msg):
    """Get system info and send it.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
    """
    await msg.channel.send(
        f'Я работаю на '
        f'**{system()} {release()}** *({version()})*, '
        f'у которого процессор *({processor()})* '
        f'имеет архитектуру - **{machine()}**', delete_after=DELAY_TIME
    )
    await sleep(DELAY_TIME)
    await msg.delete()
