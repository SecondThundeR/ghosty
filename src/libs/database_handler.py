"""SQL Database Handler Library (Beta).

This script allows the user to work with a SQL database with basic functions
that only require the necessary data from the user

The module can accept strings as single queries or records
of single data to the database, and lists of strings as multiple queries
or records of several data at once

**Noteworthy:** Module returns custom exception on every SQL failure to
prevent the main script from making sudden errors

This file can also be imported as a module and contains the following functions:
    * clear_data_on_execution - clears specific tables
    * is_data_in_database - returns True or False depending on the data existence
    * get_data_from_database - returns list of data from table
    * add_data_to_database - returns True or False on the commit of data
    * edit_data_to_database - returns True or False on the edit of data
    * delete_data_in_database - returns True or False on the deletion of data
"""


import sqlite3

DATABASE_PATH = 'src/data/botDB.db'


def _connect_database(path):
    """Connect to local database.

    Parameters:
        path (str): Path to local database

    Returns:
        List which includes connection and cursor objects of database
    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return [connection, cursor]


def _disconnect_database(connection):
    """Close connection with local database.

    Parameters:
        connection (list): List which includes currently opened connection
        and cursor objects of database
    """
    connection[0].close()


def clear_data_on_execution():
    """Clear specific tables in the database.

    **Noteworthy:** This function is necessary for the internal work of the bot,
    when main script is executed
    """
    edit_data_in_database('variables',
                          ['poll_locked', 'spammer_ID', 'spammer_count'],
                          [0, 0, 0]
                          )
    remove_data_from_database('users')
    remove_data_from_database('bots')


def is_data_in_database(table, keys, data, where_statement='AND'):
    """Execute get_data_from_database to check data existence.

    Parameters:
        table (str): Name of the table
        keys (str or list[str]): Keys of the table
        data (str or int or list[str or int]): Data of the columns.
            Defaults to None
        where_statement (str): Statement for WHERE in SQL request.
            Defaults to 'AND'

    Returns:
        True if data is exists in database, False otherwise
    """
    if get_data_from_database(table, keys, data, where_statement) is None:
        return False
    return True


def get_data_from_database(table, keys, data=None, where_statement='AND'):
    """Retrieve data from a database and return it as an array.

    Parameters:
        table (str): Name of the table
        keys (str or list[str]): Keys of the table
        data (str or int or list[str or int]): Data of the columns.
            Defaults to None
        where_statement (str): Statement for WHERE in SQL request.
            Defaults to 'AND'

    Returns:
        Array with data from database.
            None if SQL request returns empty result

    Raises:
        Exception: Returns info about error
    """
    data_array = []
    temp_array = []
    try:
        database_connection = _connect_database(DATABASE_PATH)
        if isinstance(keys, str):
            if data is None:
                database_connection[1].execute(
                    f'SELECT {keys} '
                    f'FROM {table}'
                )
            elif isinstance(data, list):
                for i, _ in enumerate(data):
                    temp_array.append(f"{keys} = '{data[i]}'")
                data_to_find = " OR ".join(temp_array)
                database_connection[1].execute(
                    f"SELECT * "
                    f"FROM {table} "
                    f"WHERE {data_to_find}"
                )
            else:
                database_connection[1].execute(
                    f"SELECT * "
                    f"FROM {table} "
                    f"WHERE {keys} = '{data}'"
                )
        else:
            if data is None:
                selected_keys = ", ".join(keys)
                database_connection[1].execute(
                    f'SELECT {selected_keys} '
                    f'FROM {table}'
                )
            elif isinstance(data, (str, int)):
                for i, _ in enumerate(keys):
                    temp_array.append(f"{keys[i]} = '{data}'")
                data_to_find = f" {where_statement} ".join(temp_array)
                database_connection[1].execute(
                    f"SELECT * "
                    f"FROM {table} "
                    f"WHERE {data_to_find}"
                )
            else:
                for i, _ in enumerate(keys):
                    temp_array.append(f"{keys[i]} = '{data[i]}'")
                data_to_get = f" {where_statement} ".join(temp_array)
                database_connection[1].execute(
                    f"SELECT * "
                    f"FROM {table} "
                    f"WHERE {data_to_get}"
                )
        received_data = database_connection[1].fetchall()
        _disconnect_database(database_connection)
        for element in received_data:
            if len(element) > 1:
                for item in element:
                    data_array.append(item)
            else:
                data_array.append(element[0])
        if len(data_array) == 0:
            return None
        return data_array
    except sqlite3.Error as database_error:
        raise Exception from database_error


def add_data_to_database(table, keys, data):
    """Add data from the database and return the result of executing an SQL query.

    Parameters:
        table (str): Name of the table
        keys (str or list[str]): Keys of the table
        data (str or int or list[str or int]): Data to add to the columns

    Returns:
        True on successful commit to database, False otherwise

    Raises:
        Exception: Returns info about error
    """
    try:
        database_connection = _connect_database(DATABASE_PATH)
        if isinstance(keys, str):
            database_connection[1].execute(
                f"INSERT INTO {table} "
                f"VALUES ('{data}')"
            )
            database_connection[0].commit()
            commit_completed = True
        else:
            if len(keys) < len(data):
                for key in keys:
                    for item in data:
                        database_connection[1].execute(
                            f"INSERT INTO {table} ('{key}') "
                            f"VALUES ('{item}')"
                        )
                database_connection[0].commit()
                commit_completed = True
            elif len(keys) > len(data):
                commit_completed = False
            else:
                selected_keys = "', '".join(keys)
                data_to_add = "', '".join(data)
                database_connection[1].execute(
                    f"INSERT INTO "
                    f"{table} ('{selected_keys}') "
                    f"VALUES ('{data_to_add}')"
                )
                database_connection[0].commit()
                commit_completed = True
        _disconnect_database(database_connection)
        return commit_completed
    except sqlite3.Error as database_error:
        raise Exception from database_error


def edit_data_in_database(table, keys, data, statement=False):
    """Edit data in the database and return the status of SQL query execution.

    Parameters:
        table (str): Name of the table
        keys (str or list[str]): Keys of the table
        data (str or int or list[str or int]): Data to edit in the columns
        statement (bool): True adds WHERE statement in SQL query, False otherwise

    Returns:
        True on successful commit to database, False otherwise

    Raises:
        Exception: Returns info about error
    """
    temp_array = []
    commit_completed = False
    try:
        database_connection = _connect_database(DATABASE_PATH)
        if isinstance(keys, str) and isinstance(data, str):
            database_connection[1].execute(
                f"UPDATE {table} "
                f"SET {keys} = '{data}'"
            )
            database_connection[0].commit()
            commit_completed = True
        elif isinstance(keys, list):
            if len(keys) != len(data):
                commit_completed = False
            elif isinstance(data, str):
                for i, _ in enumerate(keys):
                    temp_array.append(f"{keys[i]} = '{data}'")
                data_to_edit = ",\n ".join(temp_array)
                database_connection[1].execute(
                    f'UPDATE {table} '
                    f'SET {data_to_edit}'
                )
                database_connection[0].commit()
                commit_completed = True
            else:
                if statement:
                    if len(keys) > 2 or len(data) > 2:
                        commit_completed = False
                    else:
                        database_connection[1].execute(
                            f"UPDATE {table} "
                            f"SET {keys[0]} = '{data[0]}' "
                            f"WHERE {keys[1]} = '{data[1]}'"
                        )
                        database_connection[0].commit()
                        commit_completed = True
                else:
                    for i, _ in enumerate(keys):
                        temp_array.append(f"{keys[i]} = '{data[i]}'")
                    data_to_edit = ",\n ".join(temp_array)
                    database_connection[1].execute(
                        f'UPDATE {table} '
                        f'SET {data_to_edit}'
                    )
                    database_connection[0].commit()
                    commit_completed = True
        _disconnect_database(database_connection)
        return commit_completed
    except sqlite3.Error as database_error:
        raise Exception from database_error


def remove_data_from_database(table, keys=None, data=None):
    """Remove data from the table and return the status of SQL query.

    Parameters:
        table (str): Name of the table
        keys (str or list[str]): Keys of the table.
            Defaults to None
        data (str or int or list[str or int]): Data to edit in the columns.
            Defaults to None

    Returns:
        True on successful commit to database, False otherwise

    Raises:
        Exception: Returns info about error
    """
    temp_array = []
    commit_completed = False
    try:
        database_connection = _connect_database(DATABASE_PATH)
        if keys is None and data is None:
            database_connection[1].execute(f'DELETE FROM {table}')
            database_connection[0].commit()
            commit_completed = True
        elif isinstance(keys, str) and isinstance(data, str):
            database_connection[1].execute(
                f"DELETE FROM {table} "
                f"WHERE {keys} = '{data}'"
            )
            database_connection[0].commit()
            commit_completed = True
        elif isinstance(keys, list):
            if isinstance(data, str):
                for i, _ in enumerate(keys):
                    temp_array.append(f"{keys[i]} = '{data}'")
                data_to_delete = " AND ".join(temp_array)
                database_connection[1].execute(
                    f"DELETE FROM {table} "
                    f"WHERE {data_to_delete}"
                )
                database_connection[0].commit()
                commit_completed = True
            else:
                for i, _ in enumerate(keys):
                    temp_array.append(f"{keys[i]} = '{data[i]}'")
                data_to_delete = " AND ".join(temp_array)
                database_connection[1].execute(
                    f'DELETE FROM {table} '
                    f'WHERE {data_to_delete}'
                )
                database_connection[0].commit()
                commit_completed = True
        _disconnect_database(database_connection)
        return commit_completed
    except sqlite3.Error as database_error:
        raise Exception from database_error
