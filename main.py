# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import logging
import tornado.ioloop
import tornado.web


LOGGER = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_query_argument('signature', default=None)
        timestamp = self.get_query_argument('timestamp', default=None)
        nonce = self.get_query_argument('nonce', default=None)
        echo_str = self.get_query_argument('echostr')
        LOGGER.info(timestamp)
        LOGGER.info(nonce)
        LOGGER.info(nonce)
        self.write(echo_str)


def make_app():
    return tornado.web.Application([
        (r"/wx", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
