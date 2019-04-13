#!/usr/bin/python

import redis
import uuid
import pickle
import dbbase
import dbdata

class dbdict(dbbase._dbbase):
	def __init__(self, conn, id = None, cache = True):
		dbbase._dbbase.__init__(self, conn, id, cache)

		self._keys = None
		self._cache = {}

	def keys(self):
		if self._keys is None:
			self._keys = self._get_data()

		return self._keys.keys()

	def __len__(self):
		return len(self.keys())

	def __iter__(self):
		self._iter_idx = 0

		return self

	def next(self):
		if self._iter_idx == len(self):
			raise StopIteration

		x = self.keys()[self._iter_idx]
		self._iter_idx += 1
		return x

	def _initialize(self, data):
		keys = {}

		# Set data
		for k in data.keys():
			reobj = dbbase._retype(data[k])(self._conn)
			reobj._initialize(data[k])
			keys[k] = reobj._id
			reobj._ref_inc()

		self._set(keys)

	def __getitem__(self, key):
		# First check in cache
		if self.cache and key in self._cache:
			return self._cache[key]

		if self._keys is None:
			# print "Key returned from cache"
			self._keys = keys = self._get_data()
		else:
			keys = self._keys

		if key not in keys:
			raise Exception("No existing key [%s] in dict" % key)

		ret = self._get(keys[key])

		if isinstance(ret, dbdata.dbdata):
			ret = ret._get_data()

		# Save in cache
		if self.cache:
			self._cache[key] = ret

		return ret

	def __setitem__(self, key, value):
		# Invalidate cache for given key
		if self.cache and key in self._cache:
			del self._cache[key]

		if self._keys is None:
			keys = self._get_data()
		else:
			keys = self._keys

		if isinstance(value, dbbase._dbbase):
			reobj = value
		else:
			reobj = dbbase._retype(value)(self._conn)
			reobj._initialize(value)

		if key in keys:
			self._get(keys[key])._ref_dec()

		keys[key] = reobj._id
		reobj._ref_inc()

		# Rewrite
		self._set(keys)

		# Reset cache
		self._keys = None

	def __delitem__(self, key):
		if self._keys is None:
			keys = self._get_data()
		else:
			keys = self._keys

		# Delete the reference to the key
		if self.cache and key in self._cache:
			self._cache[key]._ref_dec()
			del self._cache[key]
		else:
			self._get(keys[key])._ref_dec()

		# Delete the key
		del keys[key]

		# Rewrite
		self._set(keys)

		# Reset cache
		self._keys = None
