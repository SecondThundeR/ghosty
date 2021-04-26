"""Script for getting random answer from list.

This script gets answer from user and randomly selects
answer from list below

This file can also be imported as a module and contains the following functions:
    * roll_magic_ball - gets random answer from list and send it.
"""


from random import choice
from asyncio import sleep


MAGIC_BALL_ANSWERS = [
    'Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да',
    'Можешь быть уверен в этом', 'Мне кажется — «да»', 'Вероятнее всего',
    'Хорошие перспективы', 'Знаки говорят — «да»', 'Да', 'Пока не ясно, попробуй снова',
    'Спроси позже', 'Лучше не рассказывать', 'Сейчас нельзя предсказать',
    'Сконцентрируйся и спроси опять', 'Даже не думай', 'Мой ответ — «нет»',
    'По моим данным — «нет»', 'Перспективы не очень хорошие', 'Весьма сомнительно'
]
DELAY_TIME = 3


async def roll_magic_ball(msg, text):
    """Get random answer from list and send it.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        text (str): Question from user to answer
    """
    if not text:
        await msg.channel.send(f'{msg.author.mention}, '
                                'вы не дали мне вопроса, '
                                'чтобы я на него ответил',
                                delete_after=DELAY_TIME)
        await sleep(DELAY_TIME)
        await msg.delete()
        return                          
    else:
        answer = choice(MAGIC_BALL_ANSWERS)
        await msg.channel.send(f'{msg.author.mention}, {answer.lower()}')
        return
