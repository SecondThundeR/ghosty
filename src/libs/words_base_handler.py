"""Words base handler library.

This script allows the user to work with a words base (e.g. add new word,
restore developers word base, etc.)

This file can also be imported as a module and contains the following functions:
    * add_word - adds word to main words base
    * delete_word - removes word from main words base
    * add_roulette_word - adds word to one of four roulette game words base
    * delete_roulette_word - removes word from one of four roulette game words base
    * restore_word_base - downloads and restores word base
"""


import requests
from src.libs.database_handler import add_data_to_database
from src.libs.database_handler import remove_data_from_database
from src.libs.database_handler import is_data_in_database
from src.libs.files_handler import import_data_from_local_file
from src.libs.files_handler import delete_local_file


def add_word(word):
    """Add word to main words base.

    Parameters:
        word (str): Word to add to database

    Returns:
        str: Message about successful word addition
    """
    add_data_to_database(2, 'main_words_base', 'words', word)
    warn_msg = f'Хей, я успешно добавил слово "{word}" себе в базу!'
    return warn_msg


def delete_word(word):
    """Remove word from main words base.

    Parameters:
        word (str): Word to delete from database

    Returns:
        str: Message about successful word removal (Or not, if otherwise)
    """
    warn_msg = 'Ой, я не смог найти это слово. ' \
               'Вы уверены, что вы правильно его написали?'
    if is_data_in_database(2, 'main_words_base', 'words', word):
        remove_data_from_database(2, 'main_words_base', 'words', word)
        warn_msg = f'Хей, я успешно удалил слово "{word}" из своей базы!'
    return warn_msg


def add_roulette_word(word, base):
    """Add word to roulette game words base.

    Parameters:
        word (str): Word to add to database
        base (str): Roulette's table to modify

    Returns:
        str: Message about successful word addition
    """
    add_data_to_database(2, f'roulette_{base}_words', 'words', word)
    warn_msg = f'Хей, я успешно добавил слово "{word}" себе в базу!'
    return warn_msg


def delete_roulette_word(word, base):
    """Remove word from roulette game words base.

    Parameters:
        word (str): Word to delete from database
        base (str): Roulette's table to modify

    Returns:
        str: Message about successful word removal (Or not, if otherwise)
    """
    warn_msg = 'Ой, я не смог найти это слово. ' \
               'Вы уверены, что вы правильно его написали?'
    if is_data_in_database(2, f'roulette_{base}_words', 'words', word):
        remove_data_from_database(2, f'roulette_{base}_words', 'words', word)
        warn_msg = f'Хей, я успешно удалил слово "{word}" из своей базы!'
    return warn_msg


def restore_word_base(db_path, table, column, path, link):
    """Download and restore word base with link.

    This function allows to download .txt file and import it to database

    Parameters:
        db_path (int): Path of database to edit data
        table (str): Name of table in DB
        column (str): Name of column in table
        path (str): Path to local file of word base
        link (str): Link to latest word base

    Returns:
        bool: True if word base was imported successfully, False otherwise
    """
    if not _download_word_base_file(path, link):
        return False
    remove_data_from_database(db_path, table)
    words_array = import_data_from_local_file(path)
    for element in words_array:
        add_data_to_database(db_path, table, column, element)
    delete_local_file(path)
    return True


def _download_word_base_file(path, link):
    """Download word base by link.

    This function writes downloaded data into .txt file

    Parameters:
        path (str): Path to local file of word base
        link (str): Link to latest word base

    Returns:
        bool: True status code was 200, False - 404
    """
    r = requests.get(link)
    if r.status_code == 404:
        return False
    with open(path, 'wb') as f:
        f.write(r.content)
    return True
