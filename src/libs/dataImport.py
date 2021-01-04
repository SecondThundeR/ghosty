def dataImport(path):
    file = open(path, 'r', encoding='utf-8')
    fileData = file.read().splitlines()
    file.close()
    return fileData
