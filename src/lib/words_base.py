"""Words Base Handler Library.

This script allows the user to work with a words base (e.g. add new word,
restore developers word base, etc.)

This file can also be imported as a module and contains the following functions:
    * manage_words_table - adds/removes word to/from main words table
    * manage_r_words_tables - adds/removes word to/from
    one of four roulette game words base
    * restore_dev_base - downloads and restores dev's word base
    * import_word_file - downloads file and restores it
    * download_words_file - imports data from URL request to .txt file
    * clear_words_table - clears selected words tables in database
"""


import requests
import src.lib.database as database
import src.lib.files as files


WORDS_TABLES = [
    'main_words_base',
    'roulette_lose_words',
    'roulette_minus_words',
    'roulette_win_words',
    'roulette_zero_words'
]
FOLDER_PATHS = [
    'src/words_base/',
    'src/words_base/roulette_words/'
]
WORDS_FILENAMES = [
    f'{FOLDER_PATHS[0]}words.txt',
    f'{FOLDER_PATHS[1]}roulette_lose.txt',
    f'{FOLDER_PATHS[1]}roulette_minus.txt',
    f'{FOLDER_PATHS[1]}roulette_win.txt',
    f'{FOLDER_PATHS[1]}roulette_zero.txt'
]
MASTER_LINK = 'https://raw.githubusercontent.com/SecondThundeR/' \
              'ghosty/master/'


def manage_words_table(word, delete_mode=False):
    """Manage main words table.

    Args:
        word (str): Word to add or remove
        delete_mode (bool): Trigger for delete mode.
        If set to True, words will be deleted from table,
        otherwise - words will be added

    Returns:
        str: Function completion message or warning
    """
    requested_word = database.get_data(
        'wordsDB',
        True,
        'SELECT * FROM main_words_base WHERE words = ?',
        word
    )
    if not delete_mode:
        if not requested_word:
            database.modify_data(
                'wordsDB',
                'INSERT INTO main_words_base VALUES (?)',
                word
            )
            return f'Хей, я успешно добавил слово "{word}" себе в базу!'
        return 'Данное слово уже есть в базе данных, попробуйте добавить другое'
    if requested_word:
        database.modify_data(
            'wordsDB',
            'DELETE FROM main_words_base WHERE words = ?',
            word
        )
        return f'Хей, я успешно удалил слово "{word}" из своей базы!'
    return 'Ой, я не смог найти это слово. Убедитесь в правильности написания!'


def manage_r_words_tables(word, table, delete_mode=False):
    """Manage russian roulette word base.

    Args:
        word (str): Word to add or remove
        table (str): Table to modify
        delete_mode (bool): Trigger for delete mode
        If set to True, words will be deleted from table,
        otherwise - words will be added

    Returns:
        str: Function completion message or warning
    """
    requested_word = database.get_data(
        'wordsDB',
        True,
        f'SELECT * FROM roulette_{table}_words WHERE words = ?',
        word
    )
    if not delete_mode:
        if not requested_word:
            database.modify_data(
                'wordsDB',
                f'INSERT INTO roulette_{table}_words VALUES (?)',
                word
            )
            return f'Хей, я успешно добавил слово "{word}" себе в базу!'
        return 'Данное слово уже есть в базе данных, попробуйте добавить другое'
    if requested_word:
        database.modify_data(
            'wordsDB',
            f'DELETE FROM roulette_{table}_words WHERE words = ?',
            word
        )
        return f'Хей, я успешно удалил слово "{word}" из своей базы!'
    return 'Ой, я не смог найти это слово. Убедитесь в правильности написания!'


def restore_dev_base():
    """Restore dev's words base.

    This function initiates downloading and importing developers words
    into the database and handles folder creation and deletion

    If link is incorrect, aborts importing

    Returns:
        bool: True if words base restored successfully, False otherwise
    """
    for path in FOLDER_PATHS:
        files.create_folder(path)
    for table, path in zip(WORDS_TABLES, WORDS_FILENAMES):
        import_status = import_word_file(
            'wordsDB',
            table,
            path
        )
        if not import_status:
            return False
    files.delete_folder(FOLDER_PATHS[0])
    return True


def import_word_file(db_name, table, path):
    """Download word base by link and import it.

    This function downloads .txt file and imports it to database
    If link is incorrect, aborts importing

    Args:
        db_name (str): Name of database to edit data
        table (str): Name of table in DB
        path (str): Path to local file of word base

    Returns:
        bool: True if word base was imported successfully, False otherwise
    """
    words_download_status = download_words_file(path)
    if not words_download_status:
        return False
    words_array = files.import_data(path)
    for element in words_array:
        database.modify_data(
            db_name,
            f'INSERT INTO {table} VALUES (?)',
            element
        )
    return True


def download_words_file(path):
    """Download words file by link.

    This function writes requested data into .txt file

    Args:
        path (str): Path to local file of word base

    Returns:
        bool: True if status code was 200, False if met other status codes
    """
    r = requests.get(f'{MASTER_LINK}{path}')
    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)
        f.close()
        return True
    return False


def clear_words_table():
    """Clear words tables in database.

    This function handles deleting all data
    of selected words tables in the database

    Because of possible SQL injection, loop for tables list
    was removed
    """
    database.modify_data(
        'wordsDB',
        'DELETE FROM main_words_base; DELETE FROM roulette_lose_words; '
        'DELETE FROM roulette_minus_words; DELETE FROM roulette_win_words; '
        'DELETE FROM roulette_zero_words'
    )
