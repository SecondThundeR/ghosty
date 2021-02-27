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
    poll_data = {
        "time": 60,
        "text": "",
        "author": msg.author.mention,
        "p_votes": 0,
        "n_votes": 0
    }
    if args[0].isnumeric():
        poll_data["time"] = int(args[0])
        args.pop(0)
    poll_data["text"] = " ".join(args)
    await msg.delete()
    vote_msg = await msg.channel.send('**Время голосования от '
                                      f'{poll_data["author"]}**\n'
                                      f'Вопрос: {poll_data["text"]}\n'
                                      '*Голосование закончится через '
                                      f'{poll_data["time"]} секунд*')
    await vote_msg.add_reaction(emoji="👍")
    await vote_msg.add_reaction(emoji="👎")
    await asyncio.sleep(poll_data["time"])
    vote_msg = await vote_msg.channel.fetch_message(vote_msg.id)
    for reaction in vote_msg.reactions:
        if reaction.emoji == '👍':
            poll_data["p_votes"] = reaction.count - 1
        if reaction.emoji == '👎':
            poll_data["n_votes"] = reaction.count - 1
    await vote_msg.delete()
    if poll_data["p_votes"] > poll_data["n_votes"]:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{poll_data["text"]}** '
                               f'от {poll_data["author"]} '
                               'был принят среди многих **положительно**!\n'
                               '*Ну разве это не счастье?*')
    elif poll_data["p_votes"] < poll_data["n_votes"]:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{poll_data["text"]}** от '
                               f'{poll_data["author"]} '
                               'был принят среди многих **отрицательно**!\n'
                               '*Что ж, неудачам тоже свойственно быть*')
    elif (poll_data["p_votes"] == poll_data["n_votes"]
            and poll_data["p_votes"] > 0 and poll_data["n_votes"] > 0):
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{poll_data["text"]}** от '
                               f'{poll_data["author"]} '
                               'набрал одинаковое голосов\n'
                               'Голосование объявляется **несостоявшимся!**')
    elif poll_data["p_votes"] == 0 and poll_data["n_votes"] == 0:
        await msg.channel.send('**Голосование окончено!**\n'
                               f'Вопрос **{poll_data["text"]}** от '
                               f'{poll_data["author"]} '
                               'не получил никаких голосов\n'
                               'Голосование объявляется **несостоявшимся!**')
