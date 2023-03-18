import os

def get_current_dir():
	os.getcwd()
def new_dir(name):
	if not get_dir(name):
		os.mkdir(name)
def new_dirs(path):
	if not get_dir(path):
		os.makedirs(path)
def set_current_dir(name):
	os.chdir(name)
def back_dir():
	os.chdir("..")
def rename_file(target, new_name):
	os.rename(target, new_name)
def move_file(target, new_path):
	os.replace(target, new_path + target)
def delete_file(name):
	os.remove(name)
def delete_dir(name):
	os.rmdir(name)
def delete_dirs(path):
	os.rmdir(path)
def get_dir(name):
	return os.path.isdir(name)
def list(path = None):
	if path == None:
		return os.listdir()
	return os.listdir(path)
def size(target):
	return os.stat(target).st_size
def time(target):
	return os.stat(target).st_mtime

