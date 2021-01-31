"""Script for getting help on using the bot.

Provides a message with all available commands of bot

This file can also be imported as a module and contains the following functions:
    * send_help_message - sends message with commands of bot
"""


import asyncio

HELP_MESSAGE = 'Доступные команды бота: ' \
               '\n\n**ху** - выбирает рандомного пользователя и показывает ему ' \
               'рандомное предложение из массива слов' \
               '\n**шип** - шипперит двух рандомных пользователей и ' \
               'скрепляет их с помощью спаренного имени' \
               '\n**макар** - возвращает предложение "Улыбок тебе ' \
               'дед [перевёрнутое предложение]"' \
               '\n**рулетка** - запускает игру в русскую рулетку' \
               '\n**рандом** - получение рандомного числа' \
               '\n**йа** - аналог команды `/me`' \
               '\n**цуефа** - игра в "Камень Ножницы Бумага"' \
               '\n**полл** - создаёт простейшее голосование ' \
               'с выборами голосов "За" и "Против"' \
               '\n**хелп** - выводит информацию с командами' \
               '\n**uptime** - выводит сколько бот проработал ' \
               'с последнего запуска на сервере' \
               '\n\n*Сообщение удалится автоматически через 20 секунд*'
DELAY_TIME = 20


async def send_help_message(msg):
    """Send message with all available commands of bot.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
    """
    await msg.channel.send(HELP_MESSAGE, delete_after=DELAY_TIME)
    await asyncio.sleep(DELAY_TIME)
    await msg.delete()
