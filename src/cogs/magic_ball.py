"""Script for getting random answer from list.

This cog gets question from user and randomly selects
answer from list with answers
"""

import asyncio
import random

from discord.ext import commands


class MagicBall(commands.Cog):
    """Class to send `Magic Ball` message.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        ask_magic_ball: Gets random answer for list and sends it
    """

    def __init__(self, client):
        """Initialize variables for MagicBall.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.magic_ball_answers = [
            "Бесспорно",
            "Предрешено",
            "Никаких сомнений",
            "Определённо да",
            "Можешь быть уверен в этом",
            "Мне кажется — «да»",
            "Вероятнее всего",
            "Хорошие перспективы",
            "Знаки говорят — «да»",
            "Да",
            "Пока не ясно, попробуй снова",
            "Спроси позже",
            "Лучше не рассказывать",
            "Сейчас нельзя предсказать",
            "Сконцентрируйся и спроси опять",
            "Даже не думай",
            "Мой ответ — «нет»",
            "По моим данным — «нет»",
            "Перспективы не очень хорошие",
            "Весьма сомнительно",
        ]
        self.delay_time = 3

    @commands.command(aliases=["шар"])
    async def ask_magic_ball(self, ctx, text=None):
        """Get random answer from list and send it.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            text (Union[str, None]): Question from user to answer
            (Used only to check for existence)
        """
        if not text:
            await ctx.reply(
                "Вы не дали мне вопроса, "
                "чтобы я на него ответил",
                delete_after=self.delay_time,
            )
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
        else:
            await ctx.reply(random.choice(self.magic_ball_answers))


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(MagicBall(client))
