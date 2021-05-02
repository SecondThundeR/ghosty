"""Get random percent of who the user is.

Also, this cog allows to pass many options to execute
certain test outputs
"""


import asyncio
import random
import src.lib.users as users
from src.lib.exceptions import UsersNotFound
from discord.ext import commands


class UserChecker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 5
        self.loop_count = None
        self.count = None
        self.text = None
        self.user = None
        self.random_mode = False


    @commands.command(aliases=['тест'])
    async def regular_user_checker(self, ctx, *args):
        args = list(args)
        if not args:
            await ctx.reply('Вы не передали никаких аргументов',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
            return
        self.user = ctx.author.mention
        self.count = 1
        self.random_mode = False
        if args[0].isnumeric():
            self.count = int(args[0])
            args.pop(0)
        if args[0] == 'рандом':
            try:
                random_user = await users.get_random_user(ctx.message)
            except UsersNotFound as warning:
                await ctx.reply(f'Произошла ошибка: {warning}!')
                return
            self.user = random_user.mention
            self.random_mode = True
            args.pop(0)
        if not self.random_mode:
            if args[0].startswith('--'):
                self.user = args[0][2:]
                args.pop(0)
            if args[0].startswith('<@!'):
                user = await ctx.guild.fetch_member(args[0][3:len(args[0]) - 1])
                self.user = user.mention
                args.pop(0)
        self.text = ' '.join(args)
        percent_data = UserChecker.get_test_percent(self, self.count)
        if not self.text:
            await ctx.reply('Вы не передали текст для теста',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
            return
        final_msg = UserChecker.format_percent_to_message(
            self,
            percent_data,
            self.text,
            self.user
        )
        await ctx.send(final_msg)


    def get_test_percent(self, amount):
        if amount == 1:
            return random.randrange(0, 100)
        perc_list = []
        self.loop_count = 0
        while self.loop_count < amount:
            perc_list.append(random.randrange(0, 100))
            self.loop_count += 1
        return perc_list


    def format_percent_to_message(self, percent, text, user):
        warn_msg = 'Вы превысили лимит Discord по длине сообщения!'
        if type(user) == str:
            user = f'**{user}**'
        if type(percent) == list:
            msg = f'Журнал тестирования {user}\n\n'
            for i, perc in enumerate(percent):
                if len(msg) > 2000:
                    msg = warn_msg
                    break
                if perc == 0:
                    msg += f'**Тест {i + 1}.** Пациент сегодня не {text} :c\n'
                elif perc == 100:
                    msg += f'**Тест {i + 1}.** Кто бы мог подумать то! ' \
                           f'Пациент {text} на {perc}%\n'
                else:
                    msg += f'**Тест {i + 1}.** Пациент {text} на {perc}%\n'
            return msg
        if percent == 0:
            return f'{user} сегодня не {text} :c'
        elif percent == 100:
            return f'Кто бы мог подумать то! {user} {text} на {percent}%'
        else:
            return f'{user} {text} на {percent}%'


def setup(client):
    client.add_cog(UserChecker(client))
