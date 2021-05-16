import asyncio
import src.utils.markov_utils as markov_utils
from discord.ext import commands


class MarkovCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delay_time = 5

    @commands.command(aliases=['ген', 'марков'])
    async def send_markov_sentence(self, ctx, number=None):
        new_sentence = markov_utils.return_checked_sentence(number)
        if not new_sentence:
            await ctx.reply('Похоже, у меня недостаточно слов в базе данных :(',
                            delete_after=self.delay_time)
            await asyncio.sleep(self.delay_time)
            await ctx.message.delete()
        else:
            await ctx.reply(new_sentence)


def setup(client):
    client.add_cog(MarkovCommand(client))
