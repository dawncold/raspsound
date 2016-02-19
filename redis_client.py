# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import redis


def get_redis():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    return redis.StrictRedis(connection_pool=pool)
