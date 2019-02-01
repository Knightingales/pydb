#!/usr/bin/python

import redis
import uuid
import pickle
import rebase

class redata(rebase._rebase):
	# Data is a regular type (int or string)
	def __init__(self, conn, id = None):
		rebase._rebase.__init__(self, conn, id)

	def _initialize(self, data):
		# Set the data on creation
		self._set(data)
