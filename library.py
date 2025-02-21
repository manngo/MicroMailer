import math
'''Some useful functions:
Share & Enjoy'''

import sys, os, json
from pprint import pp

def dbug(*args, pretty=False, silent=None, **kwargs):
	if silent==True or silent==False:
		dbug.silent = silent
		return

	try:
		if dbug.silent:
			return
	except:
		dbug.silent = False

	fback = sys._getframe().f_back
	if not pretty:
		print(f'{os.path.basename(fback.f_code.co_filename)}:{fback.f_lineno}: ', *args, **kwargs)
	else:
		pp(*args)

def resourcePath(path):
	try:
		base = sys._MEIPASS
	except Exception:
		base = os.path.abspath('.')

def resource_path(relative_path):
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, relative_path)

import os, json
class Prefs:
	def __init__(self, paths=[]):
		self.path = os.path.join(os.path.expanduser('~'), *paths)

	def load(self):
		data = {}
		if os.path.isfile(self.path):
			jsonFile = open(self.path, 'rt', encoding='utf-8')
			try:
				data = json.load(jsonFile)
			except Exception:
				pass
			jsonFile.close()
		return data

	def save(self, prefs):
		os.makedirs(os.path.dirname(self.path), exist_ok=True)
		jsonFile = open(self.path, 'wt', encoding='utf-8')
		json.dump(prefs, jsonFile)
		jsonFile.close()
		return prefs


import configparser
def readIni(path):
	parser = configparser.ConfigParser()
	parser.read(path, encoding='utf-8')
	sections = parser.sections()
	inidata = {
		section: {
			key: value for key, value in parser.items(section)
		}
		for section in sections
	}
	return inidata

if __name__ == '__main__':
	dbug('default')
	dbug(silent=True)
	dbug('silent=true')
	dbug(silent=False)
	dbug('silent=false')
