"""Words Base Handler Library (Beta).

This script allows the user to work with a words base (e.g. add new word,
restore developers word base, etc.)

This file can also be imported as a module and contains the following functions:
    * manage_words - adds/removes word to main words base
    * delete_word - removes word from main words base
    * manage_r_words - adds/removes word to one of four roulette game words base
    * restore_word_base - downloads and restores word base
"""


from requests import get
from src.lib.database import get_data, modify_data
from src.lib.files import import_data


def manage_words(word, mode=None):
    """Manage main words base.

    Parameters:
        word (str): Word to add or remove
        mode (str): Mode of action (addition/deletion)

    Returns:
        str: Function completion message
    """
    if mode == 'add':
        modify_data(2, 'INSERT INTO main_words_base VALUES (?)', word)
        warn_msg = f'Хей, я успешно добавил слово "{word}" себе в базу!'
    elif mode == 'del':
        if get_data(
            2,
            True,
            'SELECT * FROM main_words_base WHERE words = ?',
            word
        ):
            modify_data(2, 'DELETE FROM main_words_base WHERE words = ?', word)
            warn_msg = f'Хей, я успешно удалил слово "{word}" из своей базы!'
        else:
            warn_msg = 'Ой, я не смог найти это слово. ' \
                       'Вы уверены, что вы правильно его написали?'
    else:
        warn_msg = 'Похоже что-то пошло не так, ' \
                   'свяжитесь с разработчиком для устранения проблемы'
    return warn_msg


def manage_r_word(word, base, mode=None):
    """Manage russian roulette word base.

    Parameters:
        word (str): Word to add or remove
        base (str): Roulette's table to modify
        mode (str): Mode of action (addition/deletion)

    Returns:
        str: Function completion message
    """
    if mode == 'add':
        modify_data(2, f'INSERT INTO roulette_{base}_words VALUES (?)', word)
        warn_msg = f'Хей, я успешно добавил слово "{word}" себе в базу!'
    elif mode == 'del':
        if get_data(
            2,
            True,
            f'SELECT * FROM roulette_{base}_words WHERE words = ?',
            word
        ):
            modify_data(2, f'DELETE FROM roulette_{base}_words WHERE words = ?', word)
            warn_msg = f'Хей, я успешно удалил слово "{word}" из своей базы!'
        else:
            warn_msg = 'Ой, я не смог найти это слово. ' \
                       'Вы уверены, что вы правильно его написали?'
    else:
        warn_msg = 'Похоже что-то пошло не так, ' \
                   'свяжитесь с разработчиком для устранения проблемы'
    return warn_msg


def restore_word_base(db_path, table, path, link):
    """Download and restore word base with link.

    This function allows to download .txt file and import it to database

    Parameters:
        db_path (int): Path of database to edit data
        table (str): Name of table in DB
        path (str): Path to local file of word base
        link (str): Link to latest word base

    Returns:
        bool: True if word base was imported successfully, False otherwise
    """
    if not _download_wb_file(path, link):
        return False
    words_array = import_data(path)
    for element in words_array:
        modify_data(
            db_path,
            f'INSERT INTO {table} VALUES (?)',
            element
        )
    return True


def _download_wb_file(path, link):
    """Download word base by link.

    This function writes downloaded data into .txt file

    Parameters:
        path (str): Path to local file of word base
        link (str): Link to latest word base

    Returns:
        bool: True if status code was 200, False if met other status codes
    """
    r = get(link)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)
        f.close()
        return True
    return False
