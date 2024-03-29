"""Utils for Markov chains (Beta).

This utils contains all needed functions to handle
operations with Markov chains generation and database things

This file can also be imported as a module and contains the following functions:
    * message_words_to_db - adds words from messages to database
    * check_message_content - checks message for correct content
    * markov_delay_handler - manages autogeneration delay of Markov chains
    * prepare_chains_data - prepares needed data for Markov chains generation
    * make_pairs - makes pairs of words from words list
    * get_start_word - gets start word for Markov chains sentence
    * generate_sentence - generates new Markov chains sentence
    * return_checked_sentence - gets generated data and joins to string
"""

import random
import re

import emoji

import src.lib.database as database

REGEX_RULE = (
    r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"
    r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+"
    r"|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
PREFIXES = ["@", ".", "!", "-", "/", "`"]
BAN_WORDS = ["<:", "<@&", "<@!", "<@"]


def message_words_to_db(words):
    """Add content of regular messages to database.

    This function takes array of words from message and adds them
    to special table for Markov chains

    Args:
        words (list): Array of words from message contents
    """
    for word in words:
        database.modify_data("wordsDB", "INSERT INTO markov_words VALUES (?)",
                             word)


def check_message_content(message_content):
    """Check for correct content to add.

    This check is need to exclude any unreleated messages, such as
    commands for bots, messages with emojis, @everyone/@here mentions
    and links. They can possibly break up something, so it's better to prevent
    them from passing through

    Args:
        message_content (str): Extracted content from message

    Returns:
        bool: State of check
    """
    check = True
    for word in PREFIXES:
        if message_content.startswith(word):
            check = False
            break
    for word in BAN_WORDS:
        if message_content.find(word) >= 0:
            check = False
            break
    if emoji.emoji_count(message_content) > 0:
        check = False
    if "@everyone" in message_content or "@here" in message_content:
        check = False
    if re.findall(REGEX_RULE, message_content):
        check = False
    if not check:
        markov_delay_handler("update")
    return check


def markov_delay_handler(mode):
    """Handle needed delay operation for Markov chains.

    This function manages delay of autogenerated message and
    updates current message counter

    Here are modes, such as:
    - Update: Updates current message counter (+1)
    - Clear: Updates delay of autogenerated message
    (Random integer from 20 to 45)
    - Get: Return delay and message counter

    If wrong mode provided or it isn't a 'get' mode, returns None

    Args:
        mode (str): Mode of delay handler

    Returns:
        Union[list, None]: List of current delay and message counter.
        If wrong mode/'update' or 'clear' mode were provided, returns None
    """
    current_delay = database.get_data("mainDB", True,
                                      "SELECT markov_delay FROM variables")
    msg_counter = database.get_data("mainDB", True,
                                    "SELECT msg_counter FROM variables")
    if mode == "update":
        database.modify_data("mainDB", "UPDATE variables SET msg_counter = ?",
                             msg_counter + 1)
    elif mode == "clear":
        database.modify_data(
            "mainDB",
            "UPDATE variables SET markov_delay = ?, msg_counter = ?",
            random.randint(60, 120),
            1,
        )
    elif mode == "get":
        return [current_delay, msg_counter]
    return None


def prepare_chains_data():
    """Prepare list of words and make dictionary.

    This function gets current list of words and make pairs and chains
    to work with

    Also it checks if current database is smaller than 80 words

    Returns:
        Union[list, bool]: List of words array and words dictionary.
        If current size of words database is small, returns False
    """
    word_dict = {}
    database_words = database.get_data("wordsDB", False,
                                       "SELECT * FROM markov_words")
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
    """Make pairs of words.

    This function makes pair from list of current words in database

    Args:
        words (list): List of current words

    Yields:
        Generator: Pairs of words
    """
    for i in range(len(words) - 1):
        yield (words[i], words[i + 1])


def get_start_word(words):
    """Get word to start with.

    **Note!** Because there is a chance that
    function cannot find any non-lowercase word,
    counter for failed attempts was introduces to break loop
    and return any randomly chosen word
    (Current limit of counter - 10 failed attempts)

    Args:
        words (list): List of words

    Returns:
        str: Randomly chosen word to start with
    """
    failed_attempts = 0
    first_word = random.choice(words)
    while first_word.islower():
        failed_attempts += 1
        if failed_attempts >= 10:
            break
        first_word = random.choice(words)
    return first_word


def generate_sentence(data):
    """Generate new Markov chains sentence.

    This data generates new sentence based on
    Markov chains algorithm

    **Note!** Current implementation is buggy and
    will be changed in future

    Args:
        data (list): List of data to work with

    Returns:
        chain (list): Generated sentence
        None: If generation failed
    """
    first_word = get_start_word(data[0])
    chain = [first_word]
    if len(data) == 3:
        n_words = data[2]
    else:
        n_words = random.randint(30, 80)
    i = 1
    fail_counter = 0
    while i < n_words:
        if len(" ".join(chain)) > 2000:
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


def return_checked_sentence(number=None):
    """Execute all functions to generate new sentence.

    This function gets all needed data and return joined
    sentence from chains list

    Also, this function can get user's number of size to
    generate. By default, function generates sentence with size
    between 30 and 80 words
    (If sentence with custom size hits limits of Discord,
    re-run generation without custom size)

    Args:
        number (int): Number of words to generate

    Returns:
        str: Joined sentence from chains list
    """
    data = prepare_chains_data()
    if isinstance(data, bool):
        return data
    if number is not None:
        data.append(int(number))
    new_sentence = generate_sentence(data)
    while not new_sentence:
        if len(data) == 3:
            data = data[:2]
        new_sentence = generate_sentence(data)
    joined_sentence = " ".join(new_sentence)
    return joined_sentence
