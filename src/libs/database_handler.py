import sqlite3

DATABASE_PATH = 'src/data/botDB.db'


def clear_data_on_execution():
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    cur.execute("""UPDATE variables
                      SET pollLocked = 0,
                          shipDate = '',
                          shipTextFull = '',
                          shipTextShort = '',
                          firstRandomUserInfo = '',
                          secondRandomUserInfo = '',
                          firstUsername = '',
                          secondUsername = '',
                          finalShipname = '',
                          shipActivated = 0,
                          shipInActive = 0,
                          spammerID = '',
                          spammerCount = 0"""
                )
    cur.execute("DELETE FROM users")
    cur.execute("DELETE FROM bots")
    conn.commit()
    return True


def get_data_from_database(table, keys, data='none'):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    received_data = []
    if isinstance(keys, str):
        if data != 'none':
            cur.execute(f"SELECT * FROM {table} WHERE {keys} = '{data}'")
        else:
            cur.execute(f'SELECT {keys} FROM {table}')
        received_data = cur.fetchall()
    else:
        if data != 'none':
            temp_array = []
            for i, _ in enumerate(keys):
                temp_array.append(f'{keys[i]} = {data[i]}')
            data_to_write = ",\n ".join(temp_array)
            cur.execute(f"SELECT * FROM {table} WHERE {keys} = '{data_to_write}'")
        else:
            selected_keys = ", ".join(keys)
            cur.execute(f'SELECT {selected_keys} FROM {table}')
            received_data = cur.fetchall()
    data_array = []
    for element in received_data:
        if len(element) > 1:
            for item in element:
                data_array.append(item)
        else:
            data_array.append(element[0])
    return data_array


def is_data_in_database(table, keys, data):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    if isinstance(keys, str) and isinstance(data, str):
        cur.execute(f"SELECT * FROM {table} WHERE {keys} = '{data}'")
    received_data = cur.fetchall()
    return bool(len(received_data != 0))


def add_data_to_database(table, keys, data):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    commit_completed = False
    if isinstance(keys, str) and isinstance(data, str):
        cur.execute(f"INSERT INTO {table} ('{keys}') VALUES ('{data}');")
        conn.commit()
        commit_completed = True
    elif len(keys) < len(data):
        for key in keys:
            for item in data:
                cur.execute(f"INSERT INTO {table} ('{key}') VALUES ('{item}');")
        conn.commit()
        commit_completed = True
    elif len(keys) > len(data):
        commit_completed = False
    else:
        selected_keys = "', '".join(keys)
        data_to_add = "', '".join(data)
        cur.execute(f"INSERT INTO {table} ('{selected_keys}') VALUES ('{data_to_add}');")
        conn.commit()
        commit_completed = True
    return commit_completed


def edit_data_in_database(table, keys, data, statement=False):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    commit_completed = False
    if isinstance(keys, str) and isinstance(data, str):
        cur.execute(f'UPDATE {table} SET {keys} = {data}')
        conn.commit()
        commit_completed = True
    elif len(keys) != len(data):
        commit_completed =  False
    else:
        if statement:
            cur.execute(f"UPDATE {table} SET {keys[0]} = '{data[0]}' WHERE {keys[1]} = '{data[1]}'")
            conn.commit()
            commit_completed = True
        else:
            temp_array = []
            for i, _ in enumerate(keys):
                temp_array.append(f'{keys[i]} = {data[i]}')
            data_to_write = ",\n ".join(temp_array)
            cur.execute(f'UPDATE {table} SET {data_to_write}')
            conn.commit()
            commit_completed = True
    return commit_completed


def delete_data_in_database(table, keys='none', data='none'):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    commit_completed = False
    if keys == 'none' and data == 'none':
        cur.execute(f'DELETE FROM {table}')
        conn.commit()
        commit_completed = True
    else:
        if isinstance(keys, str) and isinstance(data, str):
            cur.execute(f"DELETE FROM {table} WHERE {keys} = '{data}'")
            conn.commit()
            commit_completed = True
        elif isinstance(keys, list) and isinstance(data, list):
            temp_array = []
            for i, _ in enumerate(keys):
                temp_array.append(f"{keys[i]} = '{data[i]}'")
            data_to_delete = " AND ".join(temp_array)
            cur.execute(f'DELETE FROM {table} WHERE {data_to_delete}')
            conn.commit()
            commit_completed = True
        else:
            commit_completed = False
    return commit_completed
