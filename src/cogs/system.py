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
        send_system_info: Gets and sends info about host system
    """

    def __init__(self, client):
        """Initialize variables for SystemInfo.
        
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
        """Get system info and send it.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            mode (str | None): Mode of sended system info
        """
        if mode and 'фулл' in mode:
            if self.cpu != '':
                await ctx.reply('Я работаю на '
                                f'**{self.name} {self.release}** '
                                f'*({self.version})*, '
                                f'у которого процессор *({self.cpu})* '
                                f'имеет архитектуру - **{self.arch}**',
                                delete_after=self.delay_time)
            else:
                await ctx.reply('Я работаю на '
                                f'**{self.name} {self.release}** '
                                f'*({self.version})*, '
                                'у которого процессор имеет архитектуру - '
                                f'**{self.arch}**',
                                delete_after=self.delay_time)
        else:
            await ctx.reply('Я работаю на '
                            f'**{self.name} {self.release}** '
                            f'*({self.version})*, ',
                            delete_after=self.delay_time)
        await asyncio.sleep(self.delay_time)
        await ctx.message.delete()


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(SystemInfo(client))
