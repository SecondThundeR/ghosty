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
    SYS_NAME = system()
    SYS_RELEASE = release()
    SYS_VERSION = version()
    SYS_CPU = processor()
    SYS_ARCH = machine()
    if SYS_CPU != '':
        await msg.channel.send('Я работаю на '
                               f'**{SYS_NAME} {SYS_RELEASE}** *({SYS_VERSION})*, '
                               f'у которого процессор *({SYS_CPU})* '
                               f'имеет архитектуру - **{SYS_ARCH}**',
                               delete_after=DELAY_TIME)
    else:
        await msg.channel.send('Я работаю на '
                               f'**{SYS_NAME} {SYS_RELEASE}** *({SYS_VERSION})*, '
                               'у которого процессор имеет архитектуру - '
                               f'**{SYS_ARCH}**',
                               delete_after=DELAY_TIME)
    await asyncio.sleep(DELAY_TIME)
    await msg.delete()
