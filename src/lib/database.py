"""SQL Database Handler Library (Beta).

This script allows the user to work with a SQL database with basic functions
that only require the necessary data from the user to work with

The module can accept strings as single queries or records
of single data to the database, and lists of strings as multiple queries
or records of several data at once

**Noteworthy:** Module returns custom exception on every SQL failure to
prevent the main script from making sudden errors

This file can also be imported as a module and contains the following functions:
    * clear_on_load - clears specific tables on load
    * get_data - returns list of data from table
    * modify_data - operates with data by executing SQL queries
"""

from sqlite3 import connect
from sqlite3 import Error as DBError


DB_PATH = [
    './src/db/botDB.db',
    './src/db/confDB.db',
    './src/db/wordsDB.db'
]
BUILD_PATH = [
    'db/build_scripts/bot_build.sql',
    'db/build_scripts/conf_build.sql',
    'db/build_scripts/words_build.sql'
]


class Database:
    """A class to represent a database.

    Parameters:
        path (str): Path to database

    Methods:
        connect_db: Makes connection with database
        disconnect_db: Closes connection with database
    """
    def __init__(self, path):
        """Initialize all necessary variables for DB.

        This function get path to DB and connect with it

        Parameters:
            path (str): Path to database
        """
        self.path = path
        self.conn = None
        self.cur = None
        self.connect_db()

    def connect_db(self):
        """Make connection with local database."""
        self.conn = connect(self.path, check_same_thread=False)
        self.cur = self.conn.cursor()

    def disconnect_db(self):
        """Close connection with local database."""
        self.conn.close()


def clear_on_load():
    """Clear specific tables in the database.

    **Noteworthy:** This function is necessary for the internal work of the bot,
    when main script is executed
    """
    modify_data(0,
                'UPDATE variable SET poll_locked = ?, ship_in_active = ?,'
                ' spammer_ID = ?, spammer_count = ?, rsp_game_active = ?',
                0, 0, 0, 0, 0)
    modify_data(0, 'DELETE FROM bots')
    modify_data(0, 'DELETE FROM users')


def get_data(path_num, is_single, command, *data):
    """Retrieve data from a database and return it as an array.

    Parameters:
        path_num (int): Number of path in path list
        is_single (bool): Boolean for getting data w/o array
        command (str): Command to execute
        *data: Variable length list of data

    Returns:
        list | str | int: Array with data from database when executing 'fetchall'
            or single data when executing 'fetchone'

    Raises:
        Exception: Returns info about error
    """
    try:
        data_arr = []
        database = Database(DB_PATH[path_num])
        if not tuple(data):
            database.cur.execute(command)
        else:
            database.cur.execute(command, tuple(data))
        if is_single:
            received_data = database.cur.fetchone()
            database.disconnect_db()
            return received_data[0]
        else:
            received_data = database.cur.fetchall()
            database.disconnect_db()
            for element in received_data:
                if len(element) > 1:
                    for item in element:
                        data_arr.append(item)
                else:
                    data_arr.append(element[0])
            return data_arr
    except DBError as err:
        raise Exception from err


def modify_data(path_num, command, *data):
    """Modify data in the DB.

    Parameters:
        path_num (int): Number of path in path list
        command (str): Command to execute
        *data: Variable length list of data

    Raises:
        Exception: Returns info about error
    """
    try:
        database = Database(DB_PATH[path_num])
        if not tuple(data):
            database.cur.execute(command)
        else:
            database.cur.execute(command, tuple(data))
        database.conn.commit()
        database.disconnect_db()
    except DBError as database_error:
        raise Exception from database_error
