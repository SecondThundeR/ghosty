"""Words base handler library.

This script allows the user to work with a words base

Currently this library able to restore developer's word base

This file can also be imported as a module and contains the following functions:
    * restore_dev_word_base - restores developer's word base
"""
import requests
from src.libs.database_handler import add_data_to_database
from src.libs.database_handler import remove_data_from_database
from src.libs.files_handler import import_data_from_local_file
from src.libs.files_handler import check_if_local_file_exists
from src.libs.files_handler import delete_local_file


def restore_dev_word_base(table, column, link, path):
    """Download and restore latest dev's word base.

    Parameters:
        table (str): Name of table in DB
        column (str): Name of column in table
        link (str): Link to latest word base
        path (str): Path to local file of word base
    """
    _download_word_base_file(path, link)
    remove_data_from_database(table)
    words_array = import_data_from_local_file(path)
    for element in words_array:
        add_data_to_database(table, column, element)
    delete_local_file(path)


def _download_word_base_file(path, link):
    """Download dev's word base from Github.

    Parameters:
        path (str): Path to local file of word base
        link (str): Link to latest word base
    """
    if not check_if_local_file_exists(path):
        r = requests.get(link)
        with open(path, 'wb') as f:
            f.write(r.content)
