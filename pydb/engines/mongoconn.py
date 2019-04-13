#!/usr/bin/python
from conn import Conn

class MongoConn(Conn):
	def __init__(self, conn):
		self._conn = conn.content

	def set(self, id, value, unique = False):
		if unique:
			return self._conn.db.update({'id': id}, {'$setOnInsert': {'id': id, 'val': value}}, upsert = True)

		return self._conn.db.update({'id': id} , {'$set': {'id': id, 'val': value}})

	def get(self, id):
		return self._conn.db.find_one({'id': id})["val"]

	def delete(self, id):
		self._conn.db.delete_one({'id': id})

	def incr(self, id):
		self._conn.db.update({'id': id}, {'$inc': {'val': 1}})

	def decr(self, id):
		self._conn.db.update({'id': id}, {'$inc': {'val': -1}})

	def flushall(self):
		self._conn.db.delete_many({})
