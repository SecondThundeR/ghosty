"""Get info about machine, where bot is running.

This cog allows to get info about host machine
where bot is running at the moment
"""


import asyncio
import platform
from discord.ext import commands


class SystemInfo(commands.Cog):
    """Class to send message about host system.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        send_system_info: Sends info about host system
    """

    def __init__(self, client):
        """Initialize variables for SystemInfo.

        Also on initial load, it's getting all information about the host system

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delay_time = 5
        self.name = platform.system()
        self.release = platform.release()
        self.version = platform.version()
        self.cpu = platform.processor()
        self.arch = platform.machine()

    @commands.command(aliases=['система'])
    async def send_system_info(self, ctx, mode=None):
        """Send formatted info about host system.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            mode (Union[str, None]): Mode for format of system info
        """
        await ctx.reply(self.format_system_info(mode))
        await asyncio.sleep(self.delay_time)
        await ctx.message.delete()

    def format_system_info(self, mode):
        """Format system info and return it

        This function checks for several variants of system info outputs and
        returns needed one

        Args:
            mode (Union[str, None]): Mode for format of system info

        Returns:
            str: Formatted system info
        """
        if mode and mode == 'фулл':
            if self.cpu:
                return 'Я работаю на ' \
                       f'**{self.name} {self.release}** ' \
                       f'*({self.version})*, ' \
                       f'у которого процессор *({self.cpu})* ' \
                       f'имеет архитектуру - **{self.arch}**'
            return 'Я работаю на ' \
                   f'**{self.name} {self.release}** ' \
                   f'*({self.version})*, ' \
                   'у которого процессор имеет архитектуру - ' \
                   f'**{self.arch}**'
        return 'Я работаю на ' \
               f'**{self.name} {self.release}** ' \
               f'*({self.version})*, '


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(SystemInfo(client))
