# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import logging
from datetime import datetime
import requests

from utility import get_access_token
from queue import get_queue
from play import play_media

LOGGER = logging.getLogger(__name__)

MEDIA_URL_TPL = 'https://api.weixin.qq.com/cgi-bin/media/get?access_token={}&media_id={}'


def download_media(media_id, media_format):
    access_token = get_access_token()
    response = None
    try:
        response = requests.get(MEDIA_URL_TPL.format(access_token, media_id))
        response.raise_for_status()
    except Exception:
        LOGGER.info('got exception when download media: %(media_id)s', {'media_id': media_id})
    else:
        file_path = '/home/pi/raspsound/media/{}-{}.{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'), media_id, media_format)
        with open(file_path, mode='wb+') as f:
            f.write(response.content)
        q = get_queue()
        q.enqueue(play_media, file_path=file_path)
