#!/usr/bin/python
import redis
import uuid
import pickle
from engines import *
from pydb import *

## TODO: Implement mechanism to avoid loop-deletion in refcount

if __name__ == "__main__":
	import code

	conn = redis.Redis(host = "localhost", port = 6379)

	db = redisdb(conn)

	code.interact(local = {"db": db})
