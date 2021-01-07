import random
import asyncio
from src.libs import random_user, database_handler

WORDS_ARRAY = database_handler.get_data_from_database('words', ['words_array'])
DELAY_TIME = 3


async def get_random_word(msg, args):
	if len(args) == 0:
		current_user = msg.author.mention
	elif args[0] == 'рандом':
		r_user = await random_user.get_random_user(msg)
		if r_user is None:
			await msg.channel.send(f'{msg.author.mention}, похоже я не получил список пользователей и поэтому мне не кого упоминать. проверьте базу данных и попробуйте ещё раз')
			return
		current_user = r_user.mention
	else:
		current_user = args[0]
	if len(WORDS_ARRAY) == 0:
		await msg.channel.send(f'{msg.author.mention}, я пока не знаю никаких слов, однако вы можете добавить новые слова в мой словарь', delete_after=DELAY_TIME)
		await asyncio.sleep(DELAY_TIME)
		await msg.delete()
	elif check_for_spam(msg):
		await msg.channel.send(f'{msg.author.mention} куда спамиш?', delete_after=DELAY_TIME)
		await asyncio.sleep(DELAY_TIME)
		await msg.delete()
	else:
		await msg.channel.send(f'{current_user} {random.choice(WORDS_ARRAY)}')


def check_for_spam(msg):
	current_status = database_handler.get_data_from_database('variables', ['spammerID', 'spammerCount'])
	if current_status[0] == msg.author.id:
		if current_status[1] >= 3:
			database_handler.edit_data_in_database('variables', ['spammerCount'], [0])
			return True
		database_handler.edit_data_in_database('variables', ['spammerCount'], [current_status[1] + 1])
		return False
	database_handler.edit_data_in_database('variables', ['spammerID', 'spammerCount'], [msg.author.id, 1])
	return False
