"""Search *insert any word or something else here*.

This cog repeats the good old meme about search *p-word*
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
    async def user_finder_hub(self, ctx, mode=None):
        """Execute required finder mode depending on arguments.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
            mode (str | None): Mode of user finder
        """
        if not mode:
            return
        if 'пидорасов' in mode:
            await UserFinder.pidor_finder(self, ctx)

    async def pidor_finder(self, ctx):
        """Get random user and launch 'finder' of *p-word*.

        Parameters:
            ctx (commands.context.Context): Context object to execute functions
        """
        try:
            random_user = await users.get_random_user(ctx.message)
        except UsersNotFound as warning:
            await ctx.send(f'Произошла ошибка: {warning}!')
            return
        loop_count = 0
        init_msg = await ctx.send('Система поиска пидорасов активирована!')
        await asyncio.sleep(self.delay_time)
        while loop_count < 3:
            await ctx.send('*пип*')
            await asyncio.sleep(self.delay_time)
            loop_count += 1
        await init_msg.reply('Пидорас найден. '
                             f'Им оказался - {random_user.mention}')


def setup(client):
    client.add_cog(UserFinder(client))
