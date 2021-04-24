"""Send current uptime of bot.

This script handles calculating and sending current bot's uptime

This file can also be imported as a module and contains the following functions:
    * get_bot_uptime - gets current bot's uptime and sends it
"""


from time import time as curr_time
from asyncio import sleep
from datetime import timedelta
from src.lib.database import get_data
from src.utils.timedelta_formatter import format_timedelta


DELAY_TIME = 5


async def get_bot_uptime(msg):
    """Send current uptime of bot.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
    """
    curr_uptime = int(curr_time()) - get_data(
        0,
        True,
        'SELECT bot_uptime FROM variables',
    )
    time_string = format_timedelta(timedelta(seconds=curr_uptime))
    if curr_uptime < 36000:
        await msg.channel.send(f'Я не сплю уже на протяжении **0{time_string}**',
                               delete_after=DELAY_TIME)
    else:
        await msg.channel.send(f'Я не сплю уже на протяжении **{time_string}**',
                               delete_after=DELAY_TIME)
    await sleep(DELAY_TIME)
    await msg.delete()
