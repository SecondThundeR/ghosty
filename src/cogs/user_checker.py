"""Get random percent of who the user is.

Also, this cog allows to pass many options to execute
certain test outputs
"""


import discord
import asyncio
import random
import src.lib.users as users
from src.lib.exceptions import UsersNotFound
from discord.ext import commands


class UserChecker(commands.Cog):
    """Class to send message with user's test results.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        user_check_handler: Handles all operations with test data
        get_test_percent: Gets percent of user's test
        format_percent_to_message: Formats all passed data into final message
    """

    def __init__(self, client):
        """Initialize variables for UserChecker.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delay_time = 5

    @commands.command(aliases=['тест'])
    async def user_check_handler(self, ctx, *args):
        """Handler of user checking.

        This function handles all passed data and getting needed data for final message
        of test

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (User's and test data)

        Returns:
            None: If there is some errors
        """
        if not args:
            await ctx.reply('Вы не передали никаких аргументов',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
            return
        args = list(args)
        test_data = await self.parse_test_data(ctx, list(args))
        if test_data is None:
            return
        final_msg = UserChecker.format_percent_to_message(
            test_data['percent'],
            test_data['text'],
            test_data['user']
        )
        await ctx.send(final_msg)

    async def parse_test_data(self, ctx, test_args):
        """Parse arguments and return dictionary.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            test_args (list): Arguments of command

        Returns:
            dict: Dictionary with data, or empty, if there was an error
        """
        test_data = {
            "user": ctx.author,
            "text": "",
            "percent": None,
        }
        tests_count = 1
        random_user_mode = False
        if test_args[0].isnumeric():
            tests_count = int(test_args[0])
            test_args.pop(0)
        if test_args[0] == 'рандом':
            try:
                test_data['user'] = await users.get_random_user(ctx.message)
            except UsersNotFound as warning:
                await ctx.reply(f'Произошла ошибка: {warning}!',
                                delete_after=self.delay_time)
                await asyncio.sleep(self.delay_time)
                await ctx.message.delete()
                return None
            random_user_mode = True
            test_args.pop(0)
        if not random_user_mode:
            if test_args[0].startswith('<@!'):
                test_data['user'] = await ctx.guild.fetch_member(
                    test_args[0][3:len(test_args[0]) - 1]
                )
                test_args.pop(0)
            if test_args[0].startswith('--'):
                test_data['user'] = test_args[0][2:]
                test_args.pop(0)
        test_data['text'] = ' '.join(test_args)
        if not test_data['text']:
            await ctx.reply('Вы не передали текст для теста',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
            return None
        test_data['percent'] = UserChecker.get_test_percent(tests_count)
        return test_data

    @staticmethod
    def get_test_percent(amount):
        """Get percent of user's test.

        Process and returns all tests percents and average percent

        Args:
            amount (int): Number of tests

        Retuns:
            int: If there is one test to process
            list: If there is many tests to process.
        """
        if amount == 1:
            return random.randint(0, 100)
        perc_list = []
        avg_percent = 0
        i = 0
        for i in range(amount):
            perc_list.append(random.randint(0, 100))
            avg_percent += perc_list[i]
        avg_percent /= amount
        return [perc_list, avg_percent]

    @staticmethod
    def format_percent_to_message(percent_data, text, user):
        """Format all data to final message.

        **Some notes:**
        If user is string, pass getting username from Member object.
        If percent_data is list, runs loop for enumerating all tests to single message.
        If message hits discord limit, breaks loop and returns warning message

        Args:
            percent_data (Union[int, list]): Data of current user's test
            text (str): Text of current user's test
            user (Union[discord.member.Member, str]):
            Users data which is being "tested"

        Returns:
            str: Conclusion of user's test or warning message
        """
        warn_msg = 'Вы превысили лимит Discord по длине сообщения!'
        user_name = None
        if isinstance(user, str):
            user = f'**{user}**'
            user_name = user
        if isinstance(user, discord.Member):
            user_name = users.get_members_name(user)
            user = user.mention
        if isinstance(percent_data, list):
            percent_list = percent_data[0]
            avg_num = round(float(percent_data[1]), 2)
            msg = f'Журнал тестирования {user}\n\n'
            for i, perc in enumerate(percent_list):
                if len(msg) > 2000:
                    return warn_msg
                if perc == 0:
                    msg += f'*Тест {i + 1}.* **{user_name}** сегодня не {text} :c\n'
                elif perc == 100:
                    msg += f'*Тест {i + 1}.* Кто бы мог подумать то!\n' \
                           f'**{user_name}** {text} на **{perc}%**\n'
                else:
                    msg += f'*Тест {i + 1}.* **{user_name}** {text} на **{perc}%**\n'
            msg += f'\nСреднее значение всех тестов - **{avg_num}%**'
            return msg
        if percent_data == 0:
            return f'{user} сегодня не {text} :c'
        if percent_data == 100:
            return f'Кто бы мог подумать то! {user}' \
                   f'\n{text} на **{percent_data}%**'
        return f'{user} {text} на **{percent_data}%**'


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(UserChecker(client))
