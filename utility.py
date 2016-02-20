# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import logging
import xml.etree.ElementTree
import requests

from collection import DictObject, objectify
from redis_client import get_redis

LOGGER = logging.getLogger(__name__)

ACCESS_TOKEN_KEY = 'access-token'
ACCESS_TOKEN_URL_TPL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'


def get_app_config():
    with open('~/.config') as f:
        lines = f.readlines()
    return DictObject(appid=lines[0].strip(), app_secret=lines[1].strip())


def parse_xml(xmltext):
    arguments = DictObject()
    root = xml.etree.ElementTree.fromstring(xmltext)
    for e in root:
        if e.text:
            arguments[e.tag] = e.text
    return arguments


def get_access_token():
    redis = get_redis()
    access_token = redis.get(ACCESS_TOKEN_KEY)
    if access_token:
        return access_token
    response = None
    config = get_app_config()
    try:
        response = requests.get(ACCESS_TOKEN_URL_TPL.format(config.appid, config.app_secret))
        response.raise_for_status()
    except Exception:
        LOGGER.info('got exception when get access_token')
    else:
        response = objectify(response.json())
        redis.setex(ACCESS_TOKEN_KEY, response.expires_in-200, response.access_token)
        return response.access_token
