"""SQL Database Handler Library (Beta).

This script allows the user to work with a SQL database with basic functions
that only require the necessary data from the user to work with

The module can accept commands as strings and list of data to add

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
    './src/db/mainDB.db',
    './src/db/confDB.db',
    './src/db/wordsDB.db'
]


class Database:
    """A class to control database.

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
                'UPDATE variables SET poll_locked = ?, ship_in_active = ?,'
                'rsp_game_active = ?',
                0, 0, 0)
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
        list | str | int: Array with data or single data

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
        print('There is an error while working with DB.\n'
              f'Here are error details: {err}')
        raise Exception


def modify_data(path_num, command, *data):
    """Modify data in the DB.

    Parameters:
        path_num (int): Number of path in path list
        command (str): Command to execute
        data (tuple): List of data

    Raises:
        Exception: Returns info about error
    """
    try:
        database = Database(DB_PATH[path_num])
        database.cur.execute(command, data)
        database.conn.commit()
        database.disconnect_db()
    except DBError as err:
        print('There is an error while working with DB.\n'
              f'Here are error details: {err}')
        raise Exception
