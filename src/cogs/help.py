"""Send help message for using the bot.

This cog provides a message with all available commands for bot
"""


import discord
import asyncio
from discord.ext import commands


class HelpMessage(commands.Cog):
    """Class to send help message.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        on_ready: Removes built-in `help` command
        send_help_message: Sends message with commands
    """

    def __init__(self, client):
        """Initialize variables for HelpMessage.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delay_time = 5
        self.help_msg = 'Доступные команды бота: ' \
                        '\n\n**хелп** - выводит *(эту)* информацию с командами' \
                        '\n**шар** - симулятор шара с ответами' \
                        '\n**макар** - генерирует предложение "Улыбок тебе дед ...' \
                        '\n**ген** - генерирует предложение с помощью цепей Маркова' \
                        '\n**йа** - аналог команды `/me`' \
                        '\n**полл** - запускает простое голосование' \
                        '\n**рандом** - получение рандомного числа' \
                        '\n**шип** - шипперит двух рандомных пользователей' \
                        '\n**ху (who)** - рандомный пользователь + предложение' \
                        '\n**цуефа** - игра в "Камень Ножницы Бумага"' \
                        '\n**рулетка** - запускает игру в русскую рулетку' \
                        '\n**аватарка** - запускает смену текущей аватарки' \
                        '\n**система** - показывает данные о системе' \
                        '\n**аптайм** - выводит время работы бота' \
                        '\n**тест** - запускает динамическое тестирование' \
                        '\n**поиск (пидорасов)** -  *поиск пидорасов активирован...*'

    @commands.Cog.listener()
    async def on_ready(self):
        """Listener for on_ready.

        This listener is used to remove
        built-in `help` command of `discord.ext`
        """
        self.client.remove_command('help')

    @commands.command(aliases=['хелп'])
    async def send_help_message(self, ctx):
        """Send message with all available commands of bot.

        Args:
            ctx (commands.context.Context): Context object to execute functions
        """
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(self.help_msg)
        else:
            await ctx.author.send(self.help_msg)
            await ctx.reply('Хей, проверь личку! '
                            'Я отправил тебе помощь по командам',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(HelpMessage(client))
