import random
import src.lib.database as database


def message_words_to_db(words):
    for word in words:
        checked_word = check_word(word)
        if checked_word:
            database.modify_data(
                'wordsDB',
                "INSERT INTO markov_words VALUES (?)",
                checked_word
            )


def check_word(word):
    if (word.startswith('<@')
            or word.startswith('<:')
            or word.startswith('.')
            or word.startswith('!')):
        return None
    if '@everyone' in word or '@here' in word:
        return None
    return word


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


def generate_new_sentence():
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
    first_word = random.choice(database_words)
    while first_word.islower():
        chain = [first_word]
        n_words = random.randint(20, 80)
        first_word = random.choice(database_words)

        for _ in range(n_words):
            chain.append(random.choice(word_dict[chain[-1]]))
    return ' '.join(chain)


def make_pairs(words):
    for i in range(len(words) - 1):
        yield (words[i], words[i + 1])
