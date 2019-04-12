#!/usr/bin/python

import redis
import uuid
import pickle
import rebase
import redata

class relist(rebase._rebase):
	def __init__(self, conn, id = None, cache = True):
		rebase._rebase.__init__(self, conn, id, cache)

                self._cache = {}
		self._keys = None

	def append(self, data):
		if self._keys is None:
			self._keys = keys = self._get_data()
		else:
			keys = self._keys

		reobj = rebase._retype(data)(self._conn)
		reobj._initialize(data)
		keys.append(reobj._id)
		reobj._ref_inc()

		self._set(keys)

		# Invalidate cache
		self._keys = None

	def __iter__(self):
		self._iter_idx = 0

		return self

	def next(self):
		if self._iter_idx == len(self):
			raise StopIteration

		x = self[self._iter_idx]
		self._iter_idx += 1

		return x

	def __len__(self):
		return len(self._get_data())

	def _initialize(self, data):
		keys = []
		for d in data:
			reobj = rebase._retype(d)(self._conn)
			reobj._initialize(d)
			keys.append(reobj._id)
			reobj._ref_inc()

		self._set(keys)

	def __add__(self, other):
		if type(other) != list and not isinstance(other, relist):
			raise Exception("Invalid object for addition")

		for obj in other:
			self.append(obj)

		return self

	def __getitem__(self, index):
		if self._keys is None:
			self._keys = keys = self._get_data()
		else:
			keys = self._keys

		if index >= len(keys):
			raise Exception("Index %d is out of bounds" % index)

		ret = self._get(keys[index])

		if isinstance(ret, redata.redata):
			ret = ret._get_data()

		if self.cache:
			self._cache[index] = ret

		return ret

	def __setitem__(self, index, value):
		if self._keys is None:
			self._keys = keys = self._get_data()
		else:
			keys = self._keys

		if index >= len(keys):
			raise Exception("Index %d is out of bounds" % index)

		if isinstance(value, rebase._rebase):
			reobj = value
		else:
			reobj = rebase._retype(value)(self._conn)
			reobj._initialize(value)


		self._get(keys[index])._ref_dec()

		keys[index] = reobj._id
		reobj._ref_inc()

		# Rewrite
		self._set(keys)

		# Reset cache
		self._keys = None

                # Delete cached item
		if self.cache:
			del self._cache[index]
