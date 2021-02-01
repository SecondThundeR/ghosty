"""Script for sending current uptime of bot.

This script handles calculating and sending current bot's uptime

This file can also be imported as a module and contains the following functions:
    * get_uptime_message - sends message with current uptime of bot
"""


import time
import asyncio
from datetime import timedelta
from src.libs.database_handler import get_data_from_database


DELAY_TIME = 5


async def get_uptime_message(msg):
    """Send current uptime of bot.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
    """
    curr_uptime = int(time.time()) - get_data_from_database(
        0, 'variables', 'bot_uptime'
    )[0]
    time_string = str(timedelta(seconds=curr_uptime))
    if curr_uptime < 36000:
        await msg.channel.send(f'Я не сплю уже на протяжении **0{time_string}**',
                               delete_after=DELAY_TIME)
    else:
        await msg.channel.send(f'Я не сплю уже на протяжении **{time_string}**',
                               delete_after=DELAY_TIME)
    await asyncio.sleep(DELAY_TIME)
    await msg.delete()
