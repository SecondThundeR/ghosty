"""Send help message for using the bot.

This cog provides a message with all available commands for bot
"""

import asyncio

import discord
from discord.ext import commands


class HelpMessage(commands.Cog):
    """Class to send help message.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        on_ready: Removes built-in `help` command
        send_help_message: Sends message with commands
        get_help_list: Returns a list of commands
    """

    def __init__(self, client):
        """Initialize variables for HelpMessage.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delay_time = 5
        self.help_dict = {
            "хелп": "выводит эту информацию с командами",
            "шар": "симулятор шара с ответами",
            "макар": 'генерирует предложение "Улыбок тебе дед ..."',
            "ген": "генерирует предложение с помощью цепей Маркова",
            "йа": "аналог команды `/me`",
            "полл": "запускает простое голосование",
            "рандом": "получение рандомного числа",
            "шип": "шипперит двух рандомных пользователей",
            "ху": "рандомный пользователь + предложение",
            "ранобе": "генерирует новые названия ранобе с помощью цепей Маркова",
            "цуефа": 'игра в "Камень Ножницы Бумага"',
            "рулетка": "запускает игру в русскую рулетку",
            "аватарка": "запускает смену текущей аватарки",
            "система": "показывает данные о системе",
            "аптайм": "выводит время работы бота",
            "тест": "запускает динамическое тестирование",
            "поиск": '*поиск "кого-то" активирован...*',
            "очки": "управление аккаунтом с очками",
        }
        self.faq_link = ("https://github.com/SecondThundeR/ghosty"
                         "/wiki/Commands-Description#")
        self.error_text = "Данная команда не была найдена!"

    @commands.Cog.listener()
    async def on_ready(self):
        """Listener for on_ready.

        This listener is used to remove
        built-in `help` command of `discord.ext`
        """
        self.client.remove_command("help")

    @commands.command(aliases=["хелп"])
    async def send_help_message(self, ctx, command=None):
        """Send message with all available commands of bot.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            command (str | None): Command to get help message for
        """
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(self.__get_help_list(command))
            return
        await ctx.author.send(self.__get_help_list(command))
        await ctx.reply(
            "Хей, проверь личку, я отправил тебе информацию об этом!",
            delete_after=self.delay_time,
        )
        await asyncio.sleep(self.delay_time)
        await ctx.message.delete()

    def __get_help_list(self, command):
        """Return help list of commands or info about certain command.

        This function returns full help list of commands
        or just description of certain command with link to FAQ on Github.

        Args:
            command (str): Command to get help message for

        Returns:
            str: String with all commands
        """
        if command is None:
            help_msg = "Доступные команды бота:\n"
            for item in self.help_dict:
                help_msg += f"\n**{item}** - {self.help_dict[item]}"
            help_msg += (
                "\n\nПолучить подробную информацию о командах можно здесь - "
                f"<{self.faq_link[:-1]}>")
            return help_msg
        try:
            cmd_help = (
                "Короткая информация о команде:\n"
                f"**{command}** - {self.help_dict[command]}\n\n"
                "Получить больше информации об этой команде можно здесь - "
                f"<{self.faq_link}{command}>")
            return cmd_help
        except KeyError:
            return self.error_text


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(HelpMessage(client))
