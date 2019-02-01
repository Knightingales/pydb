Redis DB
========
Redis-backed Python-like multi-dimensional objects.


Quickstart
----------
Install via ``python ./setup.py install``.
Basic usage:
.. code-block:: python
    >>> import redis

    >>> import redisdb

    >>> db = redisdb.redisdb(redis.Redis(host = "localhost", port = 6379))

From now on ``db`` is a dict-like python object that can contain any type of objects.
Currently supported objects:
- dictionary
- list
- basic datatype (string, int, byte, etc...)

© 2019-? Knightingale <kg@cyberknights.io>
