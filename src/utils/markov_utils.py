import random
import re
import src.lib.database as database


REGEX_RULE = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)" \
             r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+" \
             r"|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
PREFIXES = ['<@', '<:', '.', '!', '-', '/', '`']


def message_words_to_db(words):
    for word in words:
        database.modify_data(
            'wordsDB',
            'INSERT INTO markov_words VALUES (?)',
            word
        )


def check_message_content(message_content):
    check = True
    if message_content.startswith(tuple(PREFIXES)):
        check = False
    if '@everyone' in message_content or '@here' in message_content:
        check = False
    if re.findall(REGEX_RULE, message_content):
        check = False
    if not check:
        markov_delay_handler('update')
    return check


def markov_delay_handler(mode):
    current_delay = database.get_data(
        'mainDB',
        True,
        'SELECT markov_delay FROM variables'
    )
    msg_counter = database.get_data(
        'mainDB',
        True,
        'SELECT msg_counter FROM variables'
    )
    if mode == 'update':
        database.modify_data(
            'mainDB',
            "UPDATE variables SET msg_counter = ?",
            msg_counter + 1
        )
    elif mode == 'clear':
        database.modify_data(
            'mainDB',
            "UPDATE variables SET markov_delay = ?, msg_counter = ?",
            random.randint(20, 45),
            0
        )
    elif mode == 'get':
        return [current_delay, msg_counter]
    return None


def prepare_markov_chains():
    word_dict = {}
    database_words = database.get_data(
        'wordsDB',
        False,
        "SELECT * FROM markov_words"
    )
    curr_len = len(database_words)
    if curr_len < 80:
        return False
    pair = make_pairs(database_words)
    for word_1, word_2 in pair:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]
    return [database_words, word_dict]


def make_pairs(words):
    for i in range(len(words) - 1):
        yield (words[i], words[i + 1])


def generate_sentence(data):
    first_word = get_start_word(data[0])
    chain = [first_word]
    if len(data) == 3:
        n_words = data[2]
    else:
        n_words = random.randint(30, 80)
    i = 1
    fail_counter = 0
    while i < n_words:
        if len(' '.join(chain)) > 2000:
            return chain[:len(chain) - 1]
        try:
            chain.append(random.choice(data[1][chain[-1]]))
            i += 1
        except KeyError:
            random_chain_key = random.choice(chain)
            while random_chain_key == chain[-1]:
                fail_counter += 1
                if fail_counter == 3:
                    return None
                random_chain_key = random.choice(chain)
            chain.append(random.choice(data[1][random_chain_key]))
            i += 1
    return chain


def get_start_word(words):
    first_word = random.choice(words)
    while first_word.islower():
        first_word = random.choice(words)
    return first_word


def return_checked_sentence(number):
    data = prepare_markov_chains()
    if isinstance(data, bool):
        return data
    if number and number.isnumeric():
        data.append(int(number))
    new_sentence = generate_sentence(data)
    while not new_sentence:
        if len(data) == 3:
            data = data[:2]
        new_sentence = generate_sentence(data)
    joined_sentence = ' '.join(new_sentence)
    return joined_sentence
