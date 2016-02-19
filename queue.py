# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from rq import Queue

from redis_client import get_redis

q = Queue(connection=get_redis())


def get_queue():
    return q
