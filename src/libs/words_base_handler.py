"""Words base handler library.

This script allows the user to work with a words base

Currently this library able to restore word base

This file can also be imported as a module and contains the following functions:
    * restore_word_base - imports and restores word base
"""


import requests
from src.libs.database_handler import add_data_to_database
from src.libs.database_handler import remove_data_from_database
from src.libs.files_handler import import_data_from_local_file
from src.libs.files_handler import delete_local_file


def restore_word_base(db_path, table, column, path, link):
    """Download and restore word base with link.

    Function allows to download TXT file with words and import
    it to database

    Parameters:
        db_path (int): Path of database to edit data
        table (str): Name of table in DB
        column (str): Name of column in table
        path (str): Path to local file of word base
        link (str): Link to latest word base
    """
    _download_word_base_file(path, link)
    remove_data_from_database(db_path, table)
    words_array = import_data_from_local_file(path)
    for element in words_array:
        add_data_to_database(db_path, table, column, element)
    delete_local_file(path)


def _download_word_base_file(path, link):
    """Download word base by link.

    Parameters:
        path (str): Path to local file of word base
        link (str): Link to latest word base
    """
    r = requests.get(link)
    with open(path, 'wb') as f:
        f.write(r.content)
