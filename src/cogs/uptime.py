"""Bot's uptime handler.

This cog handles calculating and sending current bot's uptime
"""


import time
import asyncio
import datetime
import src.lib.database as database
import src.utils.timedelta_formatter as td_format
from discord.ext import commands


class Uptime(commands.Cog):
    """Class to send message with uptime of bot.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        send_uptime: Gets current uptime of bot and sends it
    """

    def __init__(self, client):
        """Initialize variables for Uptime.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delay_time = 5
        self.start_time = None

    @commands.command(aliases=['аптайм'])
    async def send_uptime(self, ctx):
        """Calculate and send current uptime of bot.

        Also, it's stores bot start time in order to prevent
        from constant calls to database on each uptime request

        Args:
            ctx (commands.context.Context): Context object to execute functions
        """
        if not self.start_time:
            self.start_time = database.get_data(
                'mainDB',
                True,
                'SELECT bot_uptime FROM variables'
            )
        curr_uptime = int(time.time()) - self.start_time
        time_string = td_format.format_timedelta(
            datetime.timedelta(seconds=curr_uptime)
        )
        if curr_uptime < 36000:
            await ctx.reply(f'Я не сплю уже на протяжении **0{time_string}**',
                            delete_after=self.delay_time)
        else:
            await ctx.reply(f'Я не сплю уже на протяжении **{time_string}**',
                            delete_after=self.delay_time)
        await asyncio.sleep(self.delay_time)
        await ctx.message.delete()


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(Uptime(client))
