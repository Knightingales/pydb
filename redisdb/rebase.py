#!/usr/bin/python

import redis
import uuid
import pickle

def _retype(obj):
	import relist
	import redict
	import redata

	if type(obj) == dict:
		return redict.redict
	elif type(obj) == list:
		return relist.relist
	else:
		return redata.redata

class _rebase:
	def __init__(self, conn, id = None):
		self._conn = conn

		self._id = id
		self._create()

	def _create(self):
		if self._id is not None:
			self._conn.set(self._id, pickle.dumps(None), nx = True)
		else:
			id = str(uuid.uuid4())

			while self._conn.set(id, pickle.dumps(None), nx = True) is None:
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
		reobj = _retype(data)(self._conn)

		reobj._id = id

		return reobj
