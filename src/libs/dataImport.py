def dataImport(path):
    file = open(path, 'r', encoding='utf-8')
    return file.read().splitlines()
