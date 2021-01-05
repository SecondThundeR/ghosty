import sqlite3

databasePath = 'src/data/botDB.db'


def clearDataOnExecution():
    conn = sqlite3.connect(databasePath)
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


def getDataFromDatabase(table, keys, data='none'):
    conn = sqlite3.connect(databasePath)
    cur = conn.cursor()
    receivedData = []
    if type(keys) is str:
        if data != 'none':
            cur.execute(f"SELECT * FROM {table} WHERE {keys} = '{data}'")
        else:
            cur.execute(f'SELECT {keys} FROM {table}')
        receivedData = cur.fetchall()
    else:
        if data != 'none':
            tempArray = []
            for i, _ in enumerate(keys):
                tempArray.append(f'{keys[i]} = {data[i]}')
            dataToWrite = ",\n ".join(tempArray)
            cur.execute(f"SELECT * FROM {table} WHERE {keys} = '{dataToWrite}'")
        else:
            selectedKeys = ", ".join(keys)
            cur.execute(f'SELECT {selectedKeys} FROM {table}')
            receivedData = cur.fetchall()
    dataArray = []
    for element in receivedData:
        if len(element) > 1:
            for item in element:
                dataArray.append(item)
        else:
            dataArray.append(element[0])
    return dataArray


def isDataInDatabase(table, keys, data):
    conn = sqlite3.connect(databasePath)
    cur = conn.cursor()
    if type(keys) is str and type(data) is str:
        cur.execute(f"SELECT * FROM {table} WHERE {keys} = '{data}'")
    receivedData = cur.fetchall()
    if len(receivedData) != 0:
        return True
    else:
        return False


def addDataToDatabase(table, keys, data):
    conn = sqlite3.connect(databasePath)
    cur = conn.cursor()
    if type(keys) is str and type(data) is str:
        cur.execute(f"INSERT INTO {table} ('{keys}') VALUES ('{data}');")
        conn.commit()
        return True
    elif len(keys) < len(data):
        for key in keys:
            for item in data:
                cur.execute(f"INSERT INTO {table} ('{key}') VALUES ('{item}');")
        conn.commit()
        return True
    elif len(keys) > len(data):
        return False
    else:
        selectedKeys = "', '".join(keys)
        dataToAdd = "', '".join(data)
        cur.execute(f"INSERT INTO {table} ('{selectedKeys}') VALUES ('{dataToAdd}');")
        conn.commit()
        return True


def editDataInDatabase(table, keys, data, statement=False):
    conn = sqlite3.connect(databasePath)
    cur = conn.cursor()
    if type(keys) is str or type(data) is str:
        cur.execute(f'UPDATE {table} SET {keys} = {data}')
        conn.commit()
        return True
    elif len(keys) != len(data):
        return False
    else:
        if statement:
            cur.execute(f"UPDATE {table} SET {keys[0]} = '{data[0]}' WHERE {keys[1]} = '{data[1]}'")
            conn.commit()
            return True
        else:
            tempArray = []
            for i, _ in enumerate(keys):
                tempArray.append(f'{keys[i]} = {data[i]}')
            dataToWrite = ",\n ".join(tempArray)
            cur.execute(f'UPDATE {table} SET {dataToWrite}')
            conn.commit()
            return True


def deleteDataInDatabase(table, keys='none', data='none'):
    conn = sqlite3.connect(databasePath)
    cur = conn.cursor()
    if keys == 'none' and data == 'none':
        cur.execute(f'DELETE FROM {table}')
        conn.commit()
        return True
    else:
        if type(keys) is str and type(data) is str:
            cur.execute(f"DELETE FROM {table} WHERE {keys} = '{data}'")
            conn.commit()
            return True
        elif type(keys) is list and type(data) is list:
            tempArray = []
            for i, _ in enumerate(keys):
                tempArray.append(f"{keys[i]} = '{data[i]}'")
            dataToWrite = " AND ".join(tempArray)
            cur.execute(f'DELETE FROM {table} WHERE {dataToWrite}')
            conn.commit()
            return True
        else:
            return False
