import random
import asyncio

DELAY_TIME = 10


async def get_random_number(msg, args):
	if len(args) == 0:
		await msg.channel.send(f'{msg.author.mention}, к сожалению, я не получил аргументов для вывода рандома', delete_after=DELAY_TIME)
		await asyncio.sleep(DELAY_TIME)
		await msg.delete()
	elif len(args) == 1:
		try:
			range_number = int(args[0])
			if range_number < 1 or range_number == 1:
				await msg.channel.send(f'{msg.author.mention}, я не могу выдать рандомное число от 1 до {range_number}', delete_after=DELAY_TIME)
				await asyncio.sleep(DELAY_TIME)
				await msg.delete()
			else:
				random_number = random.randint(1, range_number)
				await msg.channel.send(f'{msg.author.mention}, ваше рандомное число от 1 до {range_number}: **{random_number}**')
		except ValueError:
			await msg.channel.send(f'{msg.author.mention}, ваш аргумент был введён неправильно', delete_after=DELAY_TIME)
			await asyncio.sleep(DELAY_TIME)
			await msg.delete()
	elif len(args) == 2:
		try:
			first_number = int(args[0])
			second_number = int(args[1])
			if first_number > second_number or first_number == second_number:
				await msg.channel.send(f'{msg.author.mention}, я не могу выдать рандомное число в диапазоне от {first_number} до {second_number}', delete_after=DELAY_TIME)
				await asyncio.sleep(DELAY_TIME)
				await msg.delete()
			else:
				random_number = random.randint(first_number, second_number)
				await msg.channel.send(f'{msg.author.mention}, ваше рандомное число от {first_number} до {second_number}: **{random_number}**')
		except ValueError:
			await msg.channel.send(f'{msg.author.mention}, ваш аргумент или аргументы были введены неправильно', delete_after=DELAY_TIME)
			await asyncio.sleep(DELAY_TIME)
			await msg.delete()
	else:
		await msg.channel.send(f'{msg.author.mention}, к сожалению, я получил аргументов больше, чем нужно, а именно `{len(args) - 2}`', delete_after=DELAY_TIME)
		await asyncio.sleep(DELAY_TIME)
		await msg.delete()
