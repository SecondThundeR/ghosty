import math
import asyncio

DELAY_TIME = 10


async def get_random_number(msg, args):
    if len(args) == 0:
        await msg.reply('к сожалению, я не получил аргументов '
                        'для вывода рандома',
                        mention_author=False, delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
    elif len(args) == 1:
        if math.isnan(args[0]):
            await msg.channel.send(f'{msg.author.mention}, аргумент был '
                                   f'введён неправильно', delete_after=DELAY_TIME)
            await asyncio.sleep(DELAY_TIME)
            await msg.delete()
        else:
            range_number = int(args[0])
            if range_number < 1:
                pass
    elif len(args) == 2:
        if math.isnan(args[0]) or math.isnan(args[1]):
            await msg.channel.send(f'{msg.author.mention}, один или два аргумента были '
                                   f'введены неправильно', delete_after=DELAY_TIME)
            await asyncio.sleep(DELAY_TIME)
            await msg.delete()
        else:
            pass
    else:
        await msg.reply(f'к сожалению, я получил аргументов больше, '
                        f'чем нужно, а именно `{len(args) - 2}`',
                        mention_author=False, delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
