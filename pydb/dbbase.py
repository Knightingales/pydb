#!/usr/bin/python

import redis
import uuid
import pickle
from engines import *

def _retype(obj):
	import dblist
	import dbdict
	import dbdata

	if type(obj) == dict:
		return dbdict.dbdict
	elif type(obj) == list:
		return dblist.dblist
	else:
		return dbdata.dbdata

class _dbbase:
	def __init__(self, conn, id = None, cache = True):
		self._conn = conn

		self.cache = cache
		self._id = id
		self._create()

	def _create(self):
		if self._id is not None:
			self._conn.set(self._id, pickle.dumps(None), unique = True)
		else:
			id = str(uuid.uuid4())

			while self._conn.set(id, pickle.dumps(None), unique = True) is None:
				id = str(uuid.uuid4())

			# Set refcount
			self._conn.set(id + "_ref", 0)

			self._id = id

	def _delete(self):
		self._conn.delete(self._id)
		self._conn.delete(self._id + "_ref")

	def _ref_inc(self):
		self._conn.incr(self._id + "_ref")

	def _ref_dec(self):
		if self._conn.decr(self._id + "_ref") == 0:
			self._delete()

	def _set(self, data):
		self._conn.set(self._id, pickle.dumps(data))

	def _get_data(self):
		return pickle.loads(self._conn.get(self._id))

	def _get(self, id):
		# Get the data
		data = pickle.loads(self._conn.get(id))

		# Decide on object type
		reobj = _retype(data)(self._conn, cache = self.cache)

		reobj._id = id

		return reobj
