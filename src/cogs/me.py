"""Send message on behalf of bot.

This cog allows you to send messages on behalf of the bot.
There are several flags that changes sending behavior
"""


from asyncio.windows_events import NULL
import src.lib.users as users
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

    @staticmethod
    def parse_me_args(ctx, args):
        """Send a user message on behalf of a bot.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): Arguments for parsing into dictionary

        Returns:
            dict: Dictionary with message data and TTS mode
        """
        if args[0] == 'анон':
            return {
                'message': ' '.join(args[1:]),
                'tts': False
            }
        if args[0] == 'анонттс':
            return {
                'message': ' '.join(args[1:]),
                'tts': True
            }
        if args[0] == 'ттс':
            return {
                'message': f'{users.get_members_name(ctx.author)}: ' \
                           f'{" ".join(args[1:])}',
                'tts': True
            }
        return {
            'message': f'{ctx.author.mention} ' \
                       f'{" ".join(args)}',
            'tts': False
        }

    @commands.command(aliases=['йа'])
    async def send_me_message(self, ctx, *args):
        """Send a user message on behalf of a bot.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): Arguments to work with (Mode + Message)
        """
        if args:
            me_data = self.parse_me_args(ctx, args)
            await ctx.message.delete()
            await ctx.send(me_data['message'], tts=me_data['tts'])


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(MeMessage(client))
