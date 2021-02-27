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
    * add_data_to_database - adds data to database
    * edit_data_to_database - edit data in database
    * delete_data_in_database - clears tables in database
"""


import sqlite3


DATABASE_PATHS = [
    'src/databases/botDB.db',
    'src/databases/configDB.db',
    'src/databases/wordsDB.db'
    ]


def _connect_database(path):
    """Connect to local database.

    Parameters:
        path (str): Path to local database

    Returns:
        list: Array which includes connection and cursor objects of database
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
    edit_data_in_database(
        0,
        'variables',
        ['poll_locked', 'ship_in_active',
         'spammer_ID', 'spammer_count',
         'rsp_game_active'],
        [0, 0, 0, 0, 0]
        )
    remove_data_from_database(0, 'bots')
    remove_data_from_database(0, 'users')


def is_data_in_database(db_path, table, keys, data, where_statement='AND'):
    """Execute get_data_from_database to check data existence.

    Parameters:
        db_path (int): Path of database to check data
        table (str): Name of the table
        keys (str or list[str]): Keys of the table
        data (str or int or list[str or int]): Data of the columns.
            Defaults to None
        where_statement (str): Statement for WHERE in SQL request.
            Defaults to 'AND'

    Returns:
        bool: True if data is exists in database, False otherwise
    """
    if get_data_from_database(db_path, table, keys, data, where_statement) == []:
        return False
    return True


def get_data_from_database(db_path, table, keys, data=None, where_statement='AND'):
    """Retrieve data from a database and return it as an array.

    Parameters:
        db_path (int): Path of database to get data
        table (str): Name of the table
        keys (str or list[str]): Keys of the table
        data (str or int or list[str or int]): Data of the columns.
            Defaults to None
        where_statement (str): Statement for WHERE in SQL request.
            Defaults to 'AND'

    Returns:
        list: Array with data from database.

    Raises:
        Exception: Returns info about error
    """
    data_array = []
    temp_array = []
    try:
        database_connection = _connect_database(DATABASE_PATHS[db_path])
        if isinstance(keys, str):
            if data is None:
                database_connection[1].execute(f'SELECT {keys} '
                                               f'FROM {table}')
            elif isinstance(data, list):
                for values in data:
                    temp_array.append(f"{keys} = '{values}'")
                data_to_find = " OR ".join(temp_array)
                database_connection[1].execute("SELECT * "
                                               f"FROM {table} "
                                               f"WHERE {data_to_find}")
            else:
                database_connection[1].execute("SELECT * "
                                               f"FROM {table} "
                                               f"WHERE {keys} = '{data}'")
        else:
            if data is None:
                selected_keys = ", ".join(keys)
                database_connection[1].execute(f'SELECT {selected_keys} '
                                               f'FROM {table}')
            elif isinstance(data, (str, int)):
                for key in keys:
                    temp_array.append(f"{key} = '{data}'")
                data_to_find = f" {where_statement} ".join(temp_array)
                database_connection[1].execute("SELECT * "
                                               f"FROM {table} "
                                               f"WHERE {data_to_find}")
            else:
                for key, value in zip(keys, data):
                    temp_array.append(f"{key} = '{value}'")
                data_to_get = f" {where_statement} ".join(temp_array)
                database_connection[1].execute("SELECT * "
                                               f"FROM {table} "
                                               f"WHERE {data_to_get}")
        received_data = database_connection[1].fetchall()
        _disconnect_database(database_connection)
        for element in received_data:
            if len(element) > 1:
                for item in element:
                    data_array.append(item)
            else:
                data_array.append(element[0])
        return data_array
    except sqlite3.Error as database_error:
        raise Exception from database_error


def add_data_to_database(db_path, table, keys, data):
    """Add data from the database and return the result of executing an SQL query.

    Parameters:
        db_path (int): Path of database to add data
        table (str): Name of the table
        keys (str or list[str]): Keys of the table
        data (str or int or list[str or int]): Data to add to the columns

    Raises:
        Exception: Returns info about error
    """
    try:
        database_connection = _connect_database(DATABASE_PATHS[db_path])
        if isinstance(keys, str):
            database_connection[1].execute(f"INSERT INTO {table} "
                                           f"VALUES ('{data}')")
            database_connection[0].commit()
        else:
            if len(keys) < len(data):
                for key in keys:
                    for item in data:
                        database_connection[1].execute(f"INSERT INTO {table} "
                                                       f"('{key}') "
                                                       f"VALUES ('{item}')")
                database_connection[0].commit()
            elif len(keys) > len(data):
                pass
            else:
                selected_keys = "', '".join(keys)
                data_to_add = "', '".join(data)
                database_connection[1].execute("INSERT INTO "
                                               f"{table} ('{selected_keys}') "
                                               f"VALUES ('{data_to_add}')")
                database_connection[0].commit()
        _disconnect_database(database_connection)
    except sqlite3.Error as database_error:
        raise Exception from database_error


def edit_data_in_database(db_path, table, keys, data, statement=False):
    """Edit data in the database and return the status of SQL query execution.

    Parameters:
        db_path (int): Path of database to edit
        table (str): Name of the table
        keys (str or list[str]): Keys of the table
        data (str or int or list[str or int]): Data to edit in the columns
        statement (bool): True adds WHERE statement in SQL query, False otherwise

    Raises:
        Exception: Returns info about error
    """
    temp_array = []
    try:
        database_connection = _connect_database(DATABASE_PATHS[db_path])
        if isinstance(keys, str) and isinstance(data, (str, int)):
            database_connection[1].execute(f"UPDATE {table} "
                                           f"SET {keys} = '{data}'")
            database_connection[0].commit()
        elif isinstance(keys, list):
            if len(keys) != len(data):
                pass
            elif isinstance(data, str):
                for key in keys:
                    temp_array.append(f"{key} = '{data}'")
                data_to_edit = ",\n ".join(temp_array)
                database_connection[1].execute(f'UPDATE {table} '
                                               f'SET {data_to_edit}')
                database_connection[0].commit()
            else:
                if statement:
                    if len(keys) > 2 or len(data) > 2:
                        pass
                    else:
                        database_connection[1].execute(f"UPDATE {table} "
                                                       f"SET {keys[0]} = '{data[0]}' "
                                                       f"WHERE {keys[1]} = '{data[1]}'")
                        database_connection[0].commit()
                else:
                    for key, value in zip(keys, data):
                        temp_array.append(f"{key} = '{value}'")
                    data_to_edit = ",\n ".join(temp_array)
                    database_connection[1].execute(f'UPDATE {table} '
                                                   f'SET {data_to_edit}')
                    database_connection[0].commit()
        _disconnect_database(database_connection)
    except sqlite3.Error as database_error:
        raise Exception from database_error


def remove_data_from_database(db_path, table, keys=None, data=None):
    """Remove data from the table and return the status of SQL query.

    Parameters:
        db_path (int): Path of database to modify
        table (str): Name of the table
        keys (str or list[str]): Keys of the table.
            Defaults to None
        data (str or int or list[str or int]): Data to edit in the columns.
            Defaults to None

    Raises:
        Exception: Returns info about error
    """
    temp_array = []
    try:
        database_connection = _connect_database(DATABASE_PATHS[db_path])
        if keys is None and data is None:
            database_connection[1].execute(f'DELETE FROM {table}')
            database_connection[0].commit()
        elif isinstance(keys, str) and isinstance(data, str):
            database_connection[1].execute(f"DELETE FROM {table} "
                                           f"WHERE {keys} = '{data}'")
            database_connection[0].commit()
        elif isinstance(keys, list):
            if isinstance(data, str):
                for key in keys:
                    temp_array.append(f"{key} = '{data}'")
                data_to_delete = " AND ".join(temp_array)
                database_connection[1].execute(f"DELETE FROM {table} "
                                               f"WHERE {data_to_delete}")
                database_connection[0].commit()
            else:
                for key, value in zip(keys, data):
                    temp_array.append(f"{key} = '{value}'")
                data_to_delete = " AND ".join(temp_array)
                database_connection[1].execute(f'DELETE FROM {table} '
                                               f'WHERE {data_to_delete}')
                database_connection[0].commit()
        _disconnect_database(database_connection)
    except sqlite3.Error as database_error:
        raise Exception from database_error
