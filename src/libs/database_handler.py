"""SQL Database Handler Library

	This script allows the user to work with a SQL database with basic functions
	that only require the necessary data from the user

	The module can accept strings as single queries or records of single data to the database,
	and arrays of strings as multiple queries or records of several data at once

	**Noteworthy:** Module returns custom exception on every SQL failure to prevent the main script from making sudden errors

	This file can also be imported as a module and contains the following functions:
		* clear_data_on_execution - clears specific tables
		* is_data_in_database - returns True or False depending on the availability of data
		* get_data_from_database - returns data list from table
		* add_data_to_database - returns True or False depending on the successful commit of data into the database
		* edit_data_to_database - returns True or False depending on the successful edit of data in the database
		* delete_data_in_database - returns True or False depending on the successful deletion of data from the database
"""

import sqlite3

DATABASE_PATH = 'src/data/botDB.db'


def _connect_database(path):
	"""Connecting to local database

	Parameters:
		path (str): Path to local database

	Returns:
		List which includes connection and cursor objects of database
	"""
	connection = sqlite3.connect(path)
	cursor = connection.cursor()
	return [connection, cursor]


def _disconnect_database(connection):
	"""Close connection with local database

	Parameters:
		connection (list): List which includes currently opened connection and cursor objects of database
	"""
	connection[0].close()


def clear_data_on_execution():
	"""Clearing specific tables in the database

	Noteworthy: This function is necessary for the internal work of the bot, when main script is executed

	Raises:
		Exception: If there is error with connection to database, returns info about error
	"""
	databaseConnection = _connect_database(DATABASE_PATH)
	try:
		databaseConnection[1].execute("""UPDATE variables
																			SET pollLocked = '0',
																			spammerID = '',
																			spammerCount = '0'"""
																	)
		databaseConnection[1].execute('DELETE FROM users')
		databaseConnection[1].execute('DELETE FROM bots')
		databaseConnection[0].commit()
		_disconnect_database(databaseConnection)
	except sqlite3.Error as e:
		raise Exception(f'An error occurred while working with the database: {e}')


def is_data_in_database(table, keys, data, where_statement='AND'):
	"""Executing SQL query request and returning a response

	Parameters:
		table (str): Name of the table
		keys (str or list[str]): Keys of the table
		data (str or int or list[str or int]): Data of the columns. Defaults to None
		where_statement (str): Statement for WHERE in SQL request. Defaults to 'AND'

	Returns:
		True if data is exists in database, False otherwise

	Raises:
		Exception: If there is error with connection to database, returns info about error
	"""
	databaseConnection = _connect_database(DATABASE_PATH)
	if isinstance(keys, str):
		databaseConnection[1].execute(f"SELECT * FROM {table} WHERE {keys} = '{data}'")
	else:
		temp_array = []
		for i, _ in enumerate(keys):
			temp_array.append(f"{keys[i]} = '{data[i]}'")
		data_to_find = f" {where_statement} ".join(temp_array)
		databaseConnection[1].execute(f"SELECT * FROM {table} WHERE {data_to_find}")
	received_data = databaseConnection[1].fetchall()
	_disconnect_database(databaseConnection)
	return bool(len(received_data))


def get_data_from_database(table, keys, data=None, where_statement='AND'):
	"""Retrieving data from a database and returning it as an array

	Parameters:
		table (str): Name of the table
		keys (str or list[str]): Keys of the table
		data (str or int or list[str or int]): Data of the columns. Defaults to None
		where_statement (str): Statement for WHERE in SQL request. Defaults to 'AND'

	Returns:
		Array with data from database. None if SQL request returns empty result

	Raises:
		Exception: If there is error with connection to database, returns info about error
	"""
	data_array = []
	try:
		databaseConnection = _connect_database(DATABASE_PATH)
		if isinstance(keys, str):
			if data is None:
				databaseConnection[1].execute(f'SELECT {keys} FROM {table}')
			else:
				databaseConnection[1].execute(f"SELECT * FROM {table} WHERE {keys} = '{data}'")
		else:
			if data is None:
				selected_keys = ", ".join(keys)
				databaseConnection[1].execute(f'SELECT {selected_keys} FROM {table}')
			else:
				temp_array = []
				for i, _ in enumerate(keys):
					temp_array.append(f"{keys[i]} = '{data[i]}'")
				data_to_get = f" {where_statement} ".join(temp_array)
				databaseConnection[1].execute(f"SELECT * FROM {table} WHERE {data_to_get}")
		received_data = databaseConnection[1].fetchall()
		_disconnect_database(databaseConnection)
		for element in received_data:
			if len(element) > 1:
				for item in element:
					data_array.append(item)
			else:
				data_array.append(element[0])
		if len(data_array) == 0:
			return None
		return data_array
	except sqlite3.Error as e:
		raise Exception(f'An error occurred while working with the database: {e}')


def add_data_to_database(table, keys, data):
	"""Adding data from the database and returning the result of executing an SQL query

	Parameters:
		table (str): Name of the table
		keys (str or list[str]): Keys of the table
		data (str or int or list[str or int]): Data to add to the columns

	Returns:
		True on successful commit to database, False otherwise

	Raises:
		Exception: If there is error with connection to database, returns info about error
	"""
	try:
		databaseConnection = _connect_database(DATABASE_PATH)
		if isinstance(keys, str):
			databaseConnection[1].execute(f"INSERT INTO {table} VALUES ('{data}')")
			databaseConnection[0].commit()
			commit_completed = True
		else:
			if len(keys) < len(data):
				for key in keys:
					for item in data:
						databaseConnection[1].execute(f"INSERT INTO {table} ('{key}') VALUES ('{item}')")
				databaseConnection[0].commit()
				commit_completed = True
			elif len(keys) > len(data):
				commit_completed = False
			else:
				selected_keys = "', '".join(keys)
				data_to_add = "', '".join(data)
				databaseConnection[1].execute(f"INSERT INTO {table} ('{selected_keys}') VALUES ('{data_to_add}')")
				databaseConnection[0].commit()
				commit_completed = True
		_disconnect_database(databaseConnection)
		return commit_completed
	except sqlite3.Error as e:
		raise Exception(f'An error occurred while working with the database: {e}')


def edit_data_in_database(table, keys, data, statement=False):
	"""Editing data in the database and returning the status of SQL query execution

	Parameters:
		table (str): Name of the table
		keys (str or list[str]): Keys of the table
		data (str or int or list[str or int]): Data to edit in the columns
		statement (bool): True adds WHERE statement in SQL query, False otherwise

	Returns:
		True on successful commit to database, False otherwise

	Raises:
		Exception: If there is error with connection to database, returns info about error
	"""
	commit_completed = False
	try:
		databaseConnection = _connect_database(DATABASE_PATH)
		if isinstance(keys, str):
			databaseConnection[1].execute(f"UPDATE {table} SET {keys} = '{data}'")
			databaseConnection[0].commit()
			commit_completed = True
		elif isinstance(keys, list):
			if len(keys) != len(data):
				commit_completed = False
			else:
				if statement:
					databaseConnection[1].execute(f"UPDATE {table} SET {keys[0]} = '{data[0]}' WHERE {keys[1]} = '{data[1]}'")
					databaseConnection[0].commit()
					commit_completed = True
				else:
					temp_array = []
					for i, _ in enumerate(keys):
						if isinstance(data[i], int):
							temp_array.append(f'{keys[i]} = {data[i]}')
						else:
							temp_array.append(f"{keys[i]} = '{data[i]}'")
					data_to_write = ",\n ".join(temp_array)
					databaseConnection[1].execute(f'UPDATE {table} SET {data_to_write}')
					databaseConnection[0].commit()
					commit_completed = True
		_disconnect_database(databaseConnection)
		return commit_completed
	except sqlite3.Error as e:
		raise Exception(f'An error occurred while working with the database: {e}')


def delete_data_in_database(table, keys=None, data=None):
	"""Removing data from the database and returning the status of SQL query execution

	Parameters:
		table (str): Name of the table
		keys (str or list[str]): Keys of the table. Defaults to None
		data (str or int or list[str or int]): Data to edit in the columns. Defaults to None

	Returns:
		True on successful commit to database, False otherwise

	Raises:
		Exception: If there is error with connection to database, returns info about error
	"""
	try:
		databaseConnection = _connect_database(DATABASE_PATH)
		if keys is None and data is None:
			databaseConnection[1].execute(f'DELETE FROM {table}')
			databaseConnection[0].commit()
			commit_completed = True
		else:
			if isinstance(keys, str):
				databaseConnection[1].execute(f"DELETE FROM {table} WHERE {keys} = '{data}'")
				databaseConnection[0].commit()
				commit_completed = True
			else:
				temp_array = []
				for i, _ in enumerate(keys):
					temp_array.append(f"{keys[i]} = '{data[i]}'")
				data_to_delete = " AND ".join(temp_array)
				databaseConnection[1].execute(f'DELETE FROM {table} WHERE {data_to_delete}')
				databaseConnection[0].commit()
				commit_completed = True
		_disconnect_database(databaseConnection)
		return commit_completed
	except sqlite3.Error as e:
		raise Exception(f'An error occurred while working with the database: {e}')
