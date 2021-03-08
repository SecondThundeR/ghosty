"""Create poll with positive and negative options.

This script can create simple message with two reactions and after some time,
collects reactions and send overcome of poll

This file can also be imported as a module and contains the following functions:
    * init_poll - creates and sends simple poll message
"""


from asyncio import sleep


async def init_poll(msg, args):
    """Initialize poll and send message with it.

    If user don't provide any arguments, function will exit

    Parameters:
        msg (discord.message.Message): Execute delete, send and add_reaction functions
        args (list): List with custom poll time and/or with poll text
    """
    class Poll:

        """A class to create poll.

        Parameters:
            author (discord.member.Member): Info about author to mention
        """

        def __init__(self, author):
            self.time = 60
            self.text = ''
            self.author = author.mention
            self.p_votes = 0
            self.n_votes = 0

    if not args:
        return
    poll = Poll(msg.author)
    if args[0].isnumeric():
        poll.time = int(args[0])
        args.pop(0)
    poll.text = " ".join(args)
    await msg.delete()
    vote_msg = await msg.channel.send('**Время голосования от '
                                      f'{poll.author}**\n'
                                      f'Вопрос: {poll.text}\n'
                                      '*Голосование закончится через '
                                      f'{poll.time} секунд*')
    await vote_msg.add_reaction(emoji="👍")
    await vote_msg.add_reaction(emoji="👎")
    await sleep(poll.time)
    vote_msg = await vote_msg.channel.fetch_message(vote_msg.id)
    for reaction in vote_msg.reactions:
        if reaction.emoji == '👍':
            poll.p_votes = reaction.count - 1
        if reaction.emoji == '👎':
            poll.n_votes = reaction.count - 1
    await vote_msg.delete()
    if poll.p_votes > poll.n_votes:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{poll.text}** '
                               f'от {poll.author} '
                               'был принят среди многих **положительно**!\n'
                               '*Ну разве это не счастье?*')
    elif poll.p_votes < poll.n_votes:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{poll.text}** от '
                               f'{poll.author} '
                               'был принят среди многих **отрицательно**!\n'
                               '*Что ж, неудачам тоже свойственно быть*')
    elif (poll.p_votes == poll.n_votes
            and poll.p_votes > 0 and poll.n_votes > 0):
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{poll.text}** от '
                               f'{poll.author} '
                               'набрал одинаковое голосов\n'
                               'Голосование объявляется **несостоявшимся!**')
    elif poll.p_votes == 0 and poll.n_votes == 0:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{poll.text}** от '
                               f'{poll.author} '
                               'не получил никаких голосов\n'
                               'Голосование объявляется **несостоявшимся!**')
