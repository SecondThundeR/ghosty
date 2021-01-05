import os


def import_data_from_file(path):
	file = open(path, 'r', encoding='utf-8')
	file_data = file.read().splitlines()
	file.close()
	return file_data


def check_if_file_exists(path):
	if os.path.exists(path):
		return True
	return False


def delete_file(path):
	if check_if_file_exists(path):
		os.remove(path)
		return True
	return False
