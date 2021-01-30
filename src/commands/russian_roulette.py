import random
import asyncio
from src.libs.database_handler import get_data_from_database


DELAY_TIME = 3


def _get_random_word(condition):
  if condition == 'win':
    win_words_list = get_data_from_database(2, 'roulette_win_words', 'words')
    return random.choice(win_words_list)
  if condition == 'lose':
    lose_words_list = get_data_from_database(2, 'roulette_lose_words', 'words')
    return random.choice(lose_words_list)
  if condition == 'zero':
    zero_words_list = get_data_from_database(2, 'roulette_zero_words', 'words')
    return random.choice(zero_words_list)
  if condition == 'minus':
    minus_words_list = get_data_from_database(2, 'roulette_minus_words', 'words')
    return random.choice(minus_words_list)


async def start_roulette(msg, args):
  bullet_list = []
  player = msg.author.mention
  deadly_bullet = 0
  bullet_count = 0

  if args == []:
    bullet_count = 1
  else:
    try:
      bullet_count = int(args[0])
    except ValueError:
      await msg.channel.send(f'{player}, похоже вы передали мне не число.'
                              '\nПопробуйте ещё раз, но уже с правильными данными')

  if bullet_count == 0:
    await msg.channel.send(f'{player}, {_get_random_word("zero")}')
  elif bullet_count < 0:
    await msg.channel.send(f'{player}, {_get_random_word("minus")}')
  elif bullet_count == 6:
    await msg.channel.send('поздравляем! '
                           'теперь у нас на одного суицидника меньше. '
                          f'им был {player}!!!')
  elif bullet_count > 6:
    await msg.channel.send(f'{player}, если вдруг ты не знаешь, то напомню!'
                            '\nПо правилам русской рулетки, '
                            'можно брать только до 6 патронов')
  else:
    for i in range(bullet_count):
      charged_section_number = random.randint(1, 6)
      if charged_section_number in bullet_count:
        i -= 1
      else:
        bullet_list.append(charged_section_number)
    deadly_bullet = random.randint(1, 6)
    if deadly_bullet in bullet_list:
      await msg.channel.send('**БАХ**')
      await asyncio.sleep(DELAY_TIME)
      await msg.edit(content=f'{player}, {_get_random_word("lose")}')
    else:
      await msg.channel.send('*тишина*')
      await asyncio.sleep(DELAY_TIME)
      await msg.edit(content=f'{player}, {_get_random_word("win")}')
