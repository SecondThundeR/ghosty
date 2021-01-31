"""Script for sending meme sentence with reversed username.

This script sends sentence 'Улыбок тебе дед ...' where at the end
reverse username goes

This file can also be imported as a module and contains the following functions:
    * send_ded_makar_message - sends message with sentence and reversed username
"""


from src.libs.user_handler import get_random_user
from src.libs.user_handler import get_members_name


def _reverse_string(word):
    """Get non-reversed string and return reversed one.

    Parameters:
        word (str): Non-reversed string

    Returns:
        str: Reversed string
    """
    reversed_string = list(word)
    reversed_string.reverse()
    return "".join(reversed_string)


async def send_ded_makar_message(msg, args):
    """Send famous (maybe) sentence.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments (Custom name or user mention)
    """
    if len(args) == 0:
        r_user = await get_random_user(msg)
        if r_user is None:
            await msg.channel.send(f'{msg.author.mention}, '
                                   'похоже я не получил список пользователей и '
                                   'поэтому мне не кого упоминать')
            return
        user = get_members_name(r_user)
    else:
        if args[0].startswith('<@&'):
            await msg.channel.send(f'{msg.author.mention}, к сожалению, '
                                   'я не могу обработать это')
            return
        if args[0].startswith('<:'):
            await msg.channel.send(f'{msg.author.mention}, '
                                   'какой блин переворот эмодзи...')
            return
        if args[0] == '@everyone' or args[0] == '@here':
            await msg.channel.send(f'{msg.author.mention}, '
                                   'похоже вы пытаетесь всунуть сюда '
                                   '`@here` или `@everyone`, зачем?')
            return
        if args[0].startswith('<@!'):
            user_id = args[0][3:len(args[0]) - 1]
            custom_member = await msg.guild.fetch_member(user_id)
            user = get_members_name(custom_member)
        else:
            user = " ".join(args)
    await msg.channel.send(f'Улыбок тебе дед {_reverse_string(user)}')
