"""Script for getting random number.

This script handles getting random number in different ranges
(From 1 to {some number} or From {some number} to {some number})

This file can also be imported as a module and contains the following functions:
    * get_random_number - sends message with randomly generated number
"""


import random
import asyncio

DELAY_TIME = 10


async def get_random_number(msg, args):
    """Get random number and return it.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        args (list): List of arguments (Range numbers)
    """
    if len(args) == 0:
        await msg.channel.send(
            f'{msg.author.mention}, к сожалению, '
            f'я не получил аргументов для вывода рандома',
            delete_after=DELAY_TIME
        )
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
    elif len(args) == 1:
        try:
            range_number = int(args[0])
            if range_number < 1 or range_number == 1:
                await msg.channel.send(
                    f'{msg.author.mention}, '
                    f'я не могу выдать рандомное число '
                    f'от 1 до {range_number}',
                    delete_after=DELAY_TIME
                )
                await asyncio.sleep(DELAY_TIME)
                await msg.delete()
            else:
                random_number = random.randint(1, range_number)
                await msg.channel.send(
                    f'{msg.author.mention}, '
                    f'ваше рандомное число '
                    f'от 1 до {range_number}: **{random_number}**'
                )
        except ValueError:
            await msg.channel.send(
                f'{msg.author.mention}, '
                f'ваш аргумент был введён неправильно',
                delete_after=DELAY_TIME
            )
            await asyncio.sleep(DELAY_TIME)
            await msg.delete()
    elif len(args) == 2:
        try:
            first_number = int(args[0])
            second_number = int(args[1])
            if first_number > second_number or first_number == second_number:
                await msg.channel.send(
                    f'{msg.author.mention}, '
                    f'я не могу выдать рандомное число '
                    f'в диапазоне от {first_number} до {second_number}',
                    delete_after=DELAY_TIME
                )
                await asyncio.sleep(DELAY_TIME)
                await msg.delete()
            else:
                random_number = random.randint(first_number, second_number)
                await msg.channel.send(f'{msg.author.mention}, '
                                       f'ваше рандомное число '
                                       f'от {first_number} до {second_number}: '
                                       f'**{random_number}**'
                                       )
        except ValueError:
            await msg.channel.send(
                f'{msg.author.mention}, '
                f'ваш аргумент или аргументы '
                f'были введены неправильно',
                delete_after=DELAY_TIME)
            await asyncio.sleep(DELAY_TIME)
            await msg.delete()
    else:
        await msg.channel.send(
            f'{msg.author.mention}, к сожалению, '
            f'я получил аргументов больше, чем нужно, '
            f'а именно `{len(args) - 2}`',
            delete_after=DELAY_TIME
        )
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
