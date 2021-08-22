"""Manage ignore list of bot.

This cog handles addition/removal id's of user to/from ignore list
"""

from discord.ext import commands

import src.lib.database as database
import src.lib.users as users


class ManageIgnoreList(commands.Cog):
    """Class to operate with ignore list.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        ignore_list_manager: Forwards to needed function
        add_ignored: Adds new user to ignore list
        remove_ignored: Removes existing user from ignore list
    """

    def __init__(self, client):
        """Initialize variables for ManageIgnoreList.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client

    @commands.command(aliases=["чс"])
    @commands.dm_only()
    async def ignore_list_manager(self, ctx, *args):
        """Check if user is admin and execute required operation.

        This function handles user checking and executing addition/deletion
        of user's ID to/from ignore list

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List with selected mode and user's ID
        """
        if len(args) == 2 and users.is_user_admin(ctx.author.id):
            if args[0] == "добавить":
                await self.__add_ignored(ctx, args[1])
            elif args[0] == "удалить":
                await self.__remove_ignored(ctx, args[1])

    async def __add_ignored(self, ctx, user_id):
        """Add user's ID to blacklist.

        This function handles addition of user's ID to ignore list

        Args:
            ctx (commands.context.Context): Context object to execute functions
            user_id (str): User's ID to ban
        """
        if users.is_user_admin(user_id):
            await ctx.reply("Я не могу заблокировать админа...")
        else:
            if users.is_user_blocked(user_id):
                await ctx.reply("Данный пользователь уже заблокирован")
            else:
                database.modify_data("mainDB",
                                     "INSERT INTO block_list VALUES (?)",
                                     user_id)
                await ctx.reply("Я успешно заблокировал этого юзера")

    async def __remove_ignored(self, ctx, user_id):
        """Remove user's ID from ignore list.

        This function handles removal of user's ID from ignore list

        Args:
            ctx (commands.context.Context): Context object to execute functions
            user_id (str): User's ID to unban
        """
        if not users.is_user_blocked(user_id):
            await ctx.reply("Данный юзер уже разблокирован")
        else:
            database.modify_data(
                "mainDB", "DELETE FROM block_list WHERE blocked_id = ?",
                user_id)
            await ctx.reply("Я успешно разблокировал этого юзера")


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(ManageIgnoreList(client))
