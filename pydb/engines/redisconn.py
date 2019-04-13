#!/usr/bin/python
import uuid
from conn import *

class RedisConn(Conn):
	def __init__(self, conn):
		self._conn = conn

	def set(self, id, value, unique = False):
			if unique:
				return self._conn.set(id, value, nx = True)

			return self._conn.set(id, value)

	def get(self, id):
		return self._conn.get(id)

	def delete(self, id):
		self._conn.delete(id)

	def incr(self, id):
		self._conn.incr(id)

	def decr(self, id):
		self._conn.decr(id)

	def flushall(self):
		self._conn.flushall()
