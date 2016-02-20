# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import logging

import time
import tornado.ioloop
import tornado.web

from utility import parse_xml
from queue import get_queue
from download import download_media


LOGGER = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_query_argument('signature', default=None)
        timestamp = self.get_query_argument('timestamp', default=None)
        nonce = self.get_query_argument('nonce', default=None)
        echo_str = self.get_query_argument('echostr')
        self.write(echo_str)

    def post(self, *args, **kwargs):
        data = parse_xml(self.request.body)
        if data.MsgType != 'voice':
            return
        q = get_queue()
        q.enqueue(download_media, media_id=data.MediaId, media_format=data.Format)
        msg = '''
        <xml>
        <ToUserName><![CDATA[{}]]></ToUserName>
        <FromUserName><![CDATA[{}]]></FromUserName>
        <CreateTime>{}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[will play]]></Content>
        </xml>
        '''.format(data.FromUserName, data.ToUserName, int(time.time()))
        self.set_header('Content-Type', 'application/xml')
        self.write(msg)


def make_app():
    return tornado.web.Application([
        (r"/wx", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
