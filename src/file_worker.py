import tkinter
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror
from tkinter import messagebox
import os
import sys


def get_os_slash():
	# Слеши в названии пути к файлу в разных oc отличаются, эта функция нужна для исправления ошибки на разных oc
	if sys.platform == 'win32' or sys.platform == 'win64':
		# Слэш в виндовс
		return"\\"
	else:
		# Слэш в unix подобных oc
		return "/"

# эта функция добавляет чиселку в конец к названию файла, если файл с указанным названием уже содержится в директории
def change_name(name):
	cwd = os.getcwd()
	slash = get_os_slash()
	i = 1
	file = cwd + slash + name + '.txt'
	file = cwd + slash + name + '.txt'
	while os.path.exists(file) is True:
		file = cwd + slash + name + '.txt'
		name = name + str(i)
		i += 1
	return name + '.txt'