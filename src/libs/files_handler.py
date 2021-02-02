"""Files Handler Library.

This is a basic self-written module to handle operations with files

**Noteworthy:** As the script and needs grow, this module can be expanded and improved

This file can also be imported as a module and contains the following functions:
    * import_data_from_file - imports data from file to variable
    * check_for_file_existence - returns a boolean when checking for local file
    * create_local_folder - returns a boolean when creating a local folder
    * delete_local_file - returns a boolean when deleting a local file
    * delete_local_folder - returns a boolean when deleting a local folder
"""


import os


def import_data_from_local_file(path):
    """Import data from local file and returning as variable.

    Parameters:
        path (str): Path to local file

    Returns:
        str: Read data from local file
    """
    with open(path, 'r', encoding='utf-8') as file:
        file_data = file.read().splitlines()
    file.close()
    return file_data


def check_for_file_existence(path):
    """Check for the presence of a file at the specified path.

    Parameters:
        path (str): Path to local file

    Returns:
        bool: True if file exists, False otherwise
    """
    if os.path.exists(path):
        return True
    return False


def create_local_folder(path):
    """Create folder at the specified path.

    Parameters:
        path (str): Path to local folder
    """
    try:
        os.mkdir(path)
    except OSError:
        print('There is an error while creating folder. Skipping...')


def delete_local_file(path):
    """Delete file at the specified path.

    If file exists, removes it. Otherwise do nothing

    Parameters:
        path (str): Path to local file
    """
    if os.path.exists(path):
        os.remove(path)


def delete_local_folder(path):
    """Delete folder at the specified path.

    Parameters:
        path (str): Path to local folder
    """
    try:
        os.rmdir(path)
    except OSError:
        print('There is an error while deleting folder. Skipping...')
