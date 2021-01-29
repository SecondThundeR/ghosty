"""Files Handler Library.

This is a basic self-written module to handle operations with files

**Noteworthy:** As the script and needs grow, this module can be expanded and improved

This file can also be imported as a module and contains the following functions:
    * import_data_from_file - imports data from file to variable
    * check_if_file_exists - returns a boolean when checking a local file for existence
    * delete_file - returns a boolean when deleting a local file

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


def check_if_local_file_exists(path):
    """Check for the presence of a file at the specified path.

    Parameters:
        path (str): Path to local file

    Returns:
        bool: True if file exists, False otherwise
    """
    if os.path.exists(path):
        return True
    return False


def delete_local_file(path):
    """Delete file at the specified path.

    Parameters:
        path (str): Path to local file

    Returns:
        bool: True if the file has been deleted, False otherwise
    """
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
