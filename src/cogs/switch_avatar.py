"""Avatar switcher.

This cog allows users to change avatar of bot while it's running
with certain command.
"""


import asyncio
import datetime
import src.utils.timedelta_formatter as td_format
import src.utils.avatar_changer as avatar_changer
from discord.ext import commands


class AvatarSwitcher(commands.Cog):
    """Class to trigger avatar change by command.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        avatar_switch: Triggers avatar change
    """

    def __init__(self, client):
        """Initialize variables for AvatarSwitcher.
        
        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delay_time = 5

    @commands.command(aliases=['аватарка'])
    async def avatar_switch(self, ctx):
        """Change avatar of bot via command.

        If function gets problems with delay, sends warning about it.

        Args:
            ctx (commands.context.Context): Context object to execute functions
        """
        avatar_data = avatar_changer.get_avatar_bytes()
        if isinstance(avatar_data, int):
            time_string = td_format.format_timedelta(
                datetime.timedelta(seconds=avatar_data)
            )
            await ctx.reply('Пока что нельзя сменить аватарку. '
                            f'Попробуйте через **{time_string}**',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
        else:
            await self.client.user.edit(avatar=avatar_data)
            await ctx.reply('Аватарка успешно изменена!',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(AvatarSwitcher(client))
