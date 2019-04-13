Redis DB
========
Any DB-backed Python-like multi-dimensional objects.


Quickstart
----------
Install via ``python ./setup.py install``.

Basic usage:

.. code-block:: python

    >>> import pydb
    
    >>> import redis
    
    >>> db = pydb.pydb(pydb.RedisConn(redis.Redis(host = "localhost", port = 6379)))

    >>> import pymongo

    >>> db = pydb.pydb(pydb.MongoConn(MongoClient("mongodb://localhost:27017/")))

From now on ``db`` is a dict-like python object that can contain any type of objects.
Currently supported databases:

- Redis

- MongoDB

Currently supported objects:

- dictionary

- list

- basic datatype (string, int, byte, etc...)

© 2019-? Knightingale <kg@cyberknights.io>
