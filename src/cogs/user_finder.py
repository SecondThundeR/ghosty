"""Search *insert any word or something else here*.

This cog repeats the good old meme about search *any word*
"""


import asyncio
import src.lib.users as users
from src.lib.exceptions import UsersNotFound
from discord.ext import commands


class UserFinder(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 2

    @commands.command(aliases=['поиск'])
    async def user_finder_hub(self, ctx, word=None):
        """Execute required finder mode depending on arguments.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            word (str | None): Word for user finder
        """
        if not word:
            return
        await UserFinder.user_finder_execute(self, ctx, word)

    async def user_finder_execute(self, ctx, word):
        """Get random user and launch 'finder' of *any word*.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            word (str): Passed word to test out
        """
        try:
            random_user = await users.get_random_user(ctx.message)
        except UsersNotFound as warning:
            await ctx.send(f'Произошла ошибка: {warning}!')
            return
        i = 0
        init_msg = await ctx.send('Система поиска активирована!')
        await asyncio.sleep(self.delay_time)
        while i < 2:
            await ctx.send('*пип*')
            await asyncio.sleep(self.delay_time)
            i += 1
        await init_msg.reply(f'"{word.capitalize()}" найден. '
                             f'Им оказался - {random_user.mention}')


def setup(client):
    client.add_cog(UserFinder(client))
