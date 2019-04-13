#!/usr/bin/python

import redis
import uuid
import pickle
import dbbase

class dbdata(dbbase._dbbase):
	# Data is a regular type (int or string)
	def __init__(self, conn, id = None, cache = True):
		dbbase._dbbase.__init__(self, conn, id, cache)

	def _initialize(self, data):
		# Set the data on creation
		self._set(data)
