"""Module for sending message on behalf of bot.

This script allows you to send messages on behalf of the bot.
There are several flags that change the message sending behavior

This file can also be imported as a module and contains the following functions:
    * send_me_message - sends message on behalf of a bot
"""


async def send_me_message(msg, args):
    """Send a user message on behalf of a bot.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments to follow (Message content and/or flags)
    """
    await msg.delete()
    if len(args) >= 1:
        if args[0] == 'анон':
            args.pop(0)
            text_string = " ".join(args)
            await msg.channel.send(text_string)
        elif args[0] == 'анонттс':
            args.pop(0)
            text_string = " ".join(args)
            await msg.channel.send(text_string, tts=True)
        else:
            text_string = " ".join(args)
            await msg.channel.send(f'{msg.author.mention} {text_string}')
