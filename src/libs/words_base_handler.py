from requests import get
from src.libs.database_handler import add_data_to_database
from src.libs.database_handler import remove_data_from_database
from src.libs.file_handler import import_data_from_local_file
from src.libs.file_handler import check_if_local_file_exists
from src.libs.file_handler import delete_local_file


def restore_dev_word_base(table, column, link, path):
    _download_word_base_file(path, link)
    remove_data_from_database(table)
    words_array = import_data_from_local_file(path)
    for element in words_array:
        add_data_to_database(table, column, element)
    delete_local_file(path)


def _download_word_base_file(path, link):
    """Download dev's word base from Github."""
    if not check_if_local_file_exists(path):
        r = get(link)
        with open(path, 'wb') as f:
            f.write(r.content)
