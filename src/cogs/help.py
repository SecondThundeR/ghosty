"""Send help message for using the bot.

Provides a message with all available commands of bot

This file can also be imported as a module and contains the following functions:
    * send_help_message - sends message with commands of bot
"""


from discord import channel
from asyncio import sleep


HELP_MESSAGE = 'Доступные команды бота: ' \
               '\n\n**полл (время и текст | текст)** - запускает простое голосование' \
               '\n**макар** - возвращает предложение "Улыбок тебе ' \
               'дед [перевёрнутая строка]"' \
               '\n**хелп** - выводит информацию с командами' \
               '\n**uptime** - выводит время работы бота' \
               '\n**йа (анон | анонттс)** - аналог команды `/me`' \
               '\n**рандом (число | два числа)** - получение рандомного числа' \
               '\n**шип (два имени)** - шипперит двух рандомных пользователей' \
               '\n**цуефа** - игра в "Камень Ножницы Бумага"' \
               '\n**рулетка** - запускает игру в русскую рулетку' \
               '\n**система** - показывает данные о системе' \
               '\n**ху | who** - рандомный пользователь + рандомное предложение' \
               '\n**поиск (пидорасов)** -  *поиск пидорасов активирован...*'
DELAY_TIME = 5


async def send_help_message(msg):
    """Send message with all available commands of bot.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
    """
    if isinstance(msg.channel, channel.DMChannel):
        await msg.channel.send(HELP_MESSAGE)
    else:
        await msg.author.send(HELP_MESSAGE)
        warn_msg = await msg.channel.send(f'{msg.author.mention}, проверь личку! '
                                          'Я отправил тебе помощь по командам',
                                          delete_after=DELAY_TIME)
        await sleep(DELAY_TIME)
        await warn_msg.delete()
