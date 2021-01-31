"""Script for getting info about machine, where bot is running.

This file can also be imported as a module and contains the following functions:
    * get_system_info - retrives system info and sends it as message
"""


from platform import system, release, version, processor, machine
import asyncio


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
    await asyncio.sleep(DELAY_TIME)
    await msg.delete()
