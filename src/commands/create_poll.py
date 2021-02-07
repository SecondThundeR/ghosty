"""Script for making polls with positive and negative options.

This script can create simple message with two reactions and after some time,
collects reactions and send overcome of poll

This file can also be imported as a module and contains the following functions:
    * create_poll - creates and sends simple poll message
"""


import asyncio


async def create_poll(msg, args):
    """Create and send message with poll.

    If user don't provide any arguments, function will exit

    Parameters:
        msg (discord.message.Message): Execute delete, send and add_reaction functions
        args (list): List with custom poll time and/or with poll text
    """
    if not args:
        return
    vote_time = 60
    vote_text = ''
    vote_author = msg.author
    p_answers = 0
    n_answers = 0
    if args[0].isnumeric():
        vote_time = int(args[0])
        args.pop(0)
    vote_text = " ".join(args)
    await msg.delete()
    vote_msg = await msg.channel.send('**Время голосования от '
                                      f'{vote_author.mention}**\n'
                                      f'Вопрос: {vote_text}\n'
                                      f'*На подумать - {vote_time} секунд*')
    await vote_msg.add_reaction(emoji="👍")
    await vote_msg.add_reaction(emoji="👎")
    await asyncio.sleep(vote_time)
    vote_msg = await vote_msg.channel.fetch_message(vote_msg.id)
    for reaction in vote_msg.reactions:
        if reaction.emoji == '👍':
            p_answers = reaction.count - 1
        if reaction.emoji == '👎':
            n_answers = reaction.count - 1
    await vote_msg.delete()
    if p_answers > n_answers:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{vote_text}** от {vote_author.mention} '
                               'был принят среди многих **положительно**!\n'
                               '*Ну разве это не счастье?*')
    elif p_answers < n_answers:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{vote_text}** от {vote_author.mention} '
                               'был принят среди многих **отрицательно**!\n'
                               '*Что ж, неудачам тоже свойственно быть*')
    elif p_answers == n_answers and p_answers > 0 and n_answers > 0:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{vote_text}** от {vote_author.mention} '
                               'набрал одинаковое голосов\n'
                               'Данное голосование объявляется **несостоявшимся!**')
    elif p_answers == 0 and n_answers == 0:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{vote_text}** от {vote_author.mention} '
                               'не получил никаких голосов\n'
                               'Данное голосование объявляется **несостоявшимся!**')
