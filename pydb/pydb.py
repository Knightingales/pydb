#!/usr/bin/python

import uuid
import pickle
import dbbase
import dbdict

class pydb(dbdict.dbdict):
	def __init__(self, conn, cache = True):
		dbdict.dbdict.__init__(self, conn, "root", cache)

		# Initialize root if neccessary
		if self._get_data() is None:
			self._set({})

	def reset(self):
		self._cache = {}
		self._keys = None
		self._conn.flushall()

		# Reset the DB
		self.__init__(self._conn)
