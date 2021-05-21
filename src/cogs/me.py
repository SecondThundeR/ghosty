"""Send message on behalf of bot.

This cog allows you to send messages on behalf of the bot.
There are several flags that changes sending behavior
"""


from discord.ext import commands


class MeMessage(commands.Cog):
    """Class to send message on behalf of a bot.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        send_me_message: Sends message on behalf of a bot
    """

    def __init__(self, client):
        """Initialize variables for MeMessage.
        
        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client

    @commands.command(aliases=['йа'])
    async def send_me_message(self, ctx, *args):
        """Send a user message on behalf of a bot.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): Arguments to work with (Mode + Message)
        """
        me_data = {
            'message': '',
            'tts': False
        }
        if args:
            await ctx.message.delete()
            if args[0] == 'анон':
                me_data['message'] = " ".join(args[1:])
            elif args[0] == 'анонттс':
                me_data['message'] = " ".join(args[1:])
                me_data['tts'] = True
            elif args[0] == 'ттс':
                me_data['message'] = f'{ctx.author.mention} ' \
                                     f'{" ".join(args[1:])}'
                me_data['tts'] = True
            else:
                me_data['message'] = f'{ctx.author.mention} ' \
                                     f'{" ".join(args)}'
            await ctx.send(me_data['message'], tts=me_data['tts'])


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(MeMessage(client))
