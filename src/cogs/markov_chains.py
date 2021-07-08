"""Send new Markov chains sentence.

This cog executes Markov chains generation and sends newly generated sentence.
"""


import asyncio
import src.utils.markov_utils as markov_utils
from discord.ext import commands


class MarkovCommand(commands.Cog):
    """Class to send Markov chains sentence.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        send_markov_sentence: Gets newly generated sentence and sends it
    """

    def __init__(self, client):
        """Initialize variables for MarkovCommand.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delay_time = 5

    @commands.command(aliases=['ген'])
    async def send_markov_sentence(self, ctx, number=None):
        """Get new Markov chains sentence and send it.

        This function gets newly generated sentence and sends it.
        If database hasn't enough words to generate from, sends warning about it

        Args:
            ctx (commands.context.Context): Context object to execute functions
            number (Union[str, None]): Amount of words to generate
        """
        if number and number.isnumeric():
            new_sentence = markov_utils.return_checked_sentence(number)
        else:
            new_sentence = markov_utils.return_checked_sentence()
        if not new_sentence:
            await ctx.reply('Похоже, у меня недостаточно слов в базе данных :(',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
        else:
            await ctx.reply(new_sentence)


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(MarkovCommand(client))
