"""Avatar switcher.

This cog allows users to change avatar of bot while it's running
with certain command.
"""

import asyncio
import datetime

from discord.ext import commands

import src.utils.avatar_changer as avatar_changer
import src.utils.timedelta_formatter as td_format


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
        self.avatar_cooldown = None

    @commands.command(aliases=["аватарка"])
    async def avatar_switch(self, ctx):
        """Change avatar of bot via command.

        If function gets problems with delay, sends warning about it.

        Args:
            ctx (commands.context.Context): Context object to execute functions
        """
        avatar_data = avatar_changer.get_avatar_bytes(self.avatar_cooldown)
        if avatar_data["avatar_bytes"] is None:
            if self.avatar_cooldown is None:
                self.avatar_cooldown = avatar_data["avatar_cooldown"]
            time_string = td_format.format_timedelta(
                datetime.timedelta(seconds=avatar_data["curr_cooldown"]))
            await ctx.reply(
                "Пока что нельзя сменить аватарку. "
                f"Попробуйте через **{time_string}**",
                delete_after=self.delay_time,
            )
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
            return
        self.avatar_cooldown = avatar_data["avatar_cooldown"]
        await self.client.user.edit(avatar=avatar_data["avatar_bytes"])
        await ctx.reply("Аватарка успешно изменена!",
                        delete_after=self.delay_time)
        await asyncio.sleep(self.delay_time)
        await ctx.message.delete()


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(AvatarSwitcher(client))
