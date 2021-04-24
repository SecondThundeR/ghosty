"""Get info about machine, where bot is running.

This file can also be imported as a module and contains the following functions:
    * get_system_info - retrieves system info and sends it as message
"""


from platform import system, release, version, processor, machine
from asyncio import sleep


DELAY_TIME = 5


async def get_system_info(msg, args):
    """Get system info and send it.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): Arguments for printing full info or reduced
    """
    sys_name = system()
    sys_release = release()
    sys_version = version()
    sys_cpu = processor()
    sys_arch = machine()
    if len(args) > 0:
        if args[0] == 'фулл':
            if sys_cpu != '':
                await msg.channel.send('Я работаю на '
                                       f'**{sys_name} {sys_release}** '
                                       f'*({sys_version})*, '
                                       f'у которого процессор *({sys_cpu})* '
                                       f'имеет архитектуру - **{sys_arch}**',
                                       delete_after=DELAY_TIME)
            else:
                await msg.channel.send('Я работаю на '
                                      f'**{sys_name} {sys_release}** '
                                      f'*({sys_version})*, '
                                      'у которого процессор имеет архитектуру - '
                                      f'**{sys_arch}**',
                                      delete_after=DELAY_TIME)
            
    else:
        await msg.channel.send('Я работаю на '
                               f'**{sys_name} {sys_release}** *({sys_version})*',
                               delete_after=DELAY_TIME)
    await sleep(DELAY_TIME)
    await msg.delete()
