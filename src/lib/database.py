"""SQL Database Handler Library.

This script allows the user to work with a SQL database with basic functions
that only require the necessary data from the user to work with

The module can accept commands as strings and list of data to add

**Noteworthy:** Module returns custom exception on every SQL failure to
prevent the main script from making sudden errors

This file can also be imported as a module and contains the following functions:
    * clear_tables - clears specific tables on load
    * reset_bot_tables - clears specific tables on bot reset
    * get_data - returns list of data from table
    * modify_data - operates with data by executing SQL queries
"""

import sqlite3
import sys


class Database:
    """Class to control database.

    Args:
        path (str): Path to database

    Methods:
        connect_db: Makes connection with database
        disconnect_db: Closes connection with database
    """

    def __init__(self, db_name):
        """Initialize all necessary variables for DB.

        This function get path to DB and connect with it

        Args:
            db_name (str): Name of selected database
        """
        self.conn = None
        self.cur = None
        self.connect_db(db_name)

    def connect_db(self, selected_db):
        """Make connection with local database.

        Args:
            selected_db (str): Name of DB to connect to
        """
        self.conn = sqlite3.connect(f"./src/db/{selected_db}.db",
                                    check_same_thread=False)
        self.cur = self.conn.cursor()

    def disconnect_db(self):
        """Close connection with local database."""
        self.conn.close()


def clear_tables():
    """Clear specific tables on bot load.

    **Noteworthy:** This function is necessary for the internal work of the bot,
    when main script is executed
    """
    modify_data(
        "mainDB",
        "UPDATE variables SET poll_locked = ?, ship_in_active = ?,"
        "rsp_game_active = ?",
        0,
        0,
        0,
    )
    modify_data("mainDB", "DELETE FROM bots; DELETE FROM users")


def reset_bot_tables():
    """Clear all tables on bot reset.

    This function handles clearing all tables, when bot is resetted
    in `bot_panel`
    """
    modify_data(
        "mainDB",
        "UPDATE variables SET poll_locked = ?, ship_date = ?,"
        "ship_text_full = ?, ship_text_short = ?, ship_activated = ?,"
        "ship_in_active = ?, is_setup_completed = ?,"
        "current_selected_bot = ?, bot_uptime = ?, avatar_cooldown = ?,"
        "rsp_game_active = ?",
        0,
        0,
        "",
        "",
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    modify_data(
        "mainDB",
        "DELETE FROM bots; DELETE FROM users; DELETE FROM admin_list; "
        "DELETE FROM block_list; DELETE FROM ignored_users",
    )
    modify_data("confDB", "DELETE FROM tokens")
    modify_data(
        "wordsDB",
        "DELETE FROM main_words_base; DELETE FROM markov_words; "
        "DELETE FROM roulette_lose_words; DELETE FROM roulette_win_words; "
        "DELETE FROM roulette_zero_words;",
    )


def get_data(db_name, is_single, command, *data):
    """Retrieve data from a database and return it as an array.

    Args:
        db_name (str): Name of database to get data from
        is_single (bool): Boolean for getting data w/o array
        command (str): Command to execute
        data (tuple): Variable length list of data

    Returns:
        Union[list, str, int, None]: Array with data, single data or None

    Raises:
        Exception: Returns info about error
    """
    try:
        data_arr = []
        database = Database(db_name)
        if not data:
            database.cur.execute(command)
        else:
            database.cur.execute(command, data)
        received_data = database.cur.fetchall()
        if not received_data:
            return None
        converted_data = [item for t in received_data for item in t]
        database.disconnect_db()
        if is_single:
            if not converted_data:
                return None
            return converted_data[0]
        for element in converted_data:
            data_arr.append(element)
        return data_arr
    except sqlite3.Error as err:
        print("\nThere is an error while working with DB "
              "(Method: get_data).\n"
              f"Here are error details: {err}")
        sys.exit()


def modify_data(db_name, command, *data):
    """Modify data in the DB.

    Args:
        db_name (str): Name of database to modify data
        command (str): Command to execute
        data (tuple): List of data

    Raises:
        Exception: Returns info about error
    """
    try:
        database = Database(db_name)
        if len(data) > 0:
            database.cur.execute(command, data)
        else:
            _modify_without_data(database, command)
        database.conn.commit()
        database.disconnect_db()
    except sqlite3.Error as err:
        print("\nThere is an error while working with DB "
              "(Method: modify_data).\n"
              f"Here are error details: {err}")
        sys.exit()


def _modify_without_data(db_instance, command):
    """Make SQL querys without data tuple.

    If command contains multiple querys, then
    function will use executescript instead.

    Args:
        db_instance (Database): Database instance
        command (str): Command to execute
    """
    if command.find(";") != -1:
        db_instance.cur.executescript(command)
        return
    db_instance.cur.execute(command)
