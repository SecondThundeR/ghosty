"""Script for sending meme sentence with reversed username.

This script sends sentence 'Улыбок тебе дед ...' where at the end
reverse username goes

This file can also be imported as a module and contains the following functions:
    * send_makar_message - sends message with sentence and reversed username
"""

import emoji
import asyncio
from src.libs.user_handler import get_random_user
from src.libs.user_handler import get_members_name


DELETE_TIME = 5


async def send_makar_message(msg, args):
    """Send famous (maybe) sentence.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments (Custom name or user mention)
    """
    if not args:
        r_user = await get_random_user(msg)
        if r_user is None:
            return
        user = get_members_name(r_user)
        await msg.channel.send(f'Улыбок тебе дед {user[::-1]}')
    else:
        if emoji.emoji_count(msg.content) > 0:
            await msg.channel.send(f'{msg.author.mention}, '
                                   'какой блин шип смайлов...',
                                   delete_after=DELETE_TIME)
            await asyncio.sleep(DELETE_TIME)
            await msg.delete()
        elif args[0].startswith('<@&'):
            await msg.channel.send(f'{msg.author.mention}, к сожалению, '
                                   'я не могу обработать это',
                                   delete_after=DELETE_TIME)
            await asyncio.sleep(DELETE_TIME)
            await msg.delete()
        elif args[0].startswith('<:'):
            await msg.channel.send(f'{msg.author.mention}, '
                                   'какой блин переворот эмодзи...',
                                   delete_after=DELETE_TIME)
            await asyncio.sleep(DELETE_TIME)
            await msg.delete()
        elif '@everyone' in args[0] or '@here' in args[0]:
            await msg.channel.send(f'{msg.author.mention}, '
                                   'похоже вы пытаетесь всунуть сюда '
                                   '`@here` или `@everyone`, зачем?',
                                   delete_after=DELETE_TIME)
            await asyncio.sleep(DELETE_TIME)
            await msg.delete()
        else:
            if args[0].startswith('<@!'):
                user_id = args[0][3:len(args[0]) - 1]
                custom_member = await msg.guild.fetch_member(user_id)
                user = get_members_name(custom_member)
            else:
                user = " ".join(args)
            await msg.channel.send(f'Улыбок тебе дед {user[::-1]}')
