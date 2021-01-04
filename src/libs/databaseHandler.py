import sqlite3


def clearDataOnExecution():
    conn = sqlite3.connect("src/data/vars.db")
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
    return


def getDataFromDatabase(table, keysArray):
    conn = sqlite3.connect("src/data/vars.db")
    cur = conn.cursor()
    dataArray = []
    if len(keysArray) == 1:
        selectedKeys = keysArray[0]
    else:
        selectedKeys = ", ".join(keysArray)
    cur.execute(f'SELECT {selectedKeys} FROM {table}')
    receivedData = cur.fetchall()
    for element in receivedData:
        if len(element) > 1:
            dataArray.append(element)
        else:
            dataArray.append(element[0])
    return dataArray


# TODO: Ability to add integers
def addDataToDatabase(table, keysArray, dataArray):
    conn = sqlite3.connect("src/data/vars.db")
    cur = conn.cursor()
    if len(keysArray) != len(dataArray):
        return 'You have specified wrong keys or data array length'
    else:
        if len(keysArray) == 1 or len(dataArray) == 1:
            selectedKeys = keysArray[0]
            dataToAdd = dataArray[0]
        else:
            selectedKeys = ", ".join(keysArray)
            dataToAdd = "', '".join(dataArray)
        cur.execute(f"INSERT INTO {table} ({selectedKeys}) VALUES ('{dataToAdd}');")
        conn.commit()
        return


def editDataInDatabase(table, keysArray, dataArray):
    conn = sqlite3.connect("src/data/vars.db")
    cur = conn.cursor()
    if len(keysArray) != len(dataArray):
        return 'You have specified wrong keys or data array length'
    else:
        tempArray = []
        for i in range(len(keysArray)):
            tempArray.append(f'{keysArray[i]} = {dataArray[i]}')
        dataToWrite = ",\n ".join(tempArray)
        cur.execute(f'UPDATE {table} SET {dataToWrite}')
        conn.commit()
        return
