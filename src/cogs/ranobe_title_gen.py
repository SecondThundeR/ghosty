"""Generate random ranobe title with markovify.

This cog generates random ranobe title and sends it back.
"""

import markovify
from discord.ext import commands


class RanobeTitleGenerate(commands.Cog):
    """Class to send generated ranobe title.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        send_ranobe_title: Sends message with new ranobe title
        __generate_title: Returns generated ranobe title
    """

    def __init__(self, client):
        """Initialize variables for RanobeTitleGenerate.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.txt_path = "src/markovify_models/ranobe.txt"

    @commands.command(aliases=["ранобе"])
    async def send_ranobe_title(self, ctx, amount=None):
        """Trigger generating title and send it back.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            amount (Union[str, None]): Amount of titles to generate
        """
        await ctx.reply(self.__generate_title(amount))

    def __generate_title(self, amount):
        """Generate new title with markovify.

        Args:
            amount (str): Amount of titles to generate

        Returns:
            str: Generated Ranobe Title
        """
        with open(self.txt_path, encoding="utf8") as f:
            text = f.read()
        text_model = markovify.NewlineText(text, state_size=2)
        if amount is None:
            generated_title = text_model.make_sentence(tries=100)
            while generated_title is None:
                generated_title = text_model.make_sentence(tries=100)
            return generated_title
        new_sentences = []
        for _ in range(int(amount)):
            generated_title = text_model.make_sentence(tries=100)
            while generated_title is None:
                generated_title = text_model.make_sentence(tries=100)
            new_sentences.append(generated_title)
            if len(" ".join(new_sentences)) > 2000:
                new_sentences[: len(new_sentences) - 1]
                break
        return "\n".join(new_sentences)


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(RanobeTitleGenerate(client))
