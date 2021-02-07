"""Script for getting help on using the bot.

Provides a message with all available commands of bot

This file can also be imported as a module and contains the following functions:
    * send_help_message - sends message with commands of bot
"""


import asyncio

HELP_MESSAGE = 'Доступные команды бота: ' \
               '\n\n**полл (время и текст | текст)** - запускает простое голосование' \
               '\n**макар** - возвращает предложение "Улыбок тебе ' \
               'дед [перевёрнутое предложение]"' \
               '\n**хелп** - выводит информацию с командами' \
               '\n**uptime** - выводит сколько бот проработал ' \
               'с последнего запуска на сервере' \
               '\n**йа (анон | анонттс)** - аналог команды `/me`' \
               '\n**рандом (число | два числа)** - получение рандомного числа' \
               '\n**шип (два имени)** - шипперит двух рандомных пользователей и ' \
               'скрепляет их с помощью спаренного имени' \
               '\n**цуефа** - игра в "Камень Ножницы Бумага"' \
               '\n**рулетка** - запускает игру в русскую рулетку' \
               '\n**система** - показывает данные о системе, ' \
               'на которой запущен бот' \
               '\n**ху | who** - выбирает рандомного пользователя и показывает ему ' \
               'рандомное предложение из массива слов' \
               '\n**поиск (пидорасов)** -  *поиск пидорасов активирован...*'
DELAY_TIME = 5


async def send_help_message(msg):
    """Send message with all available commands of bot.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
    """
    await msg.author.send(HELP_MESSAGE)
    warn_message = await msg.channel.send(f'{msg.author.mention}, проверь личку! '
                                          'Я отправил тебе помощь по командам',
                                          delete_after=DELAY_TIME)
    await asyncio.sleep(DELAY_TIME)
    await warn_message.delete()
