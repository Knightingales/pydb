#!/usr/bin/python

import redis
import uuid
import pickle
import rebase
import redict

class redisdb(redict.redict):
	def __init__(self, conn):
		redict.redict.__init__(self, conn, "root")

		# Initialize root if neccessary
		if self._get_data() is None:
			self._set({})

	def reset(self):
		self._cache = {}
		self._keys = None
		self._conn.flushall()

		# Reset the DB
		self.__init__(self._conn)
