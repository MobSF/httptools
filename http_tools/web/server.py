#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Web UI and server."""
import os
import sys

import tornado

from http_tools.web.controllers.index import (
    KillHandler,
    MainHandler,
)
from http_tools.web.controllers.dashboard import (
    DashboardHandler,
    FlowMetaHandler,
    RepeatHandler,
)
import http_tools.settings as settings


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/dashboard', DashboardHandler),
            (r'/dashboard/(.*)', DashboardHandler),
            (r'/flow_meta', FlowMetaHandler),
            (r'/repeat/(.*)', RepeatHandler),
            (r'/kill', KillHandler),
        ]
        app_settings = {
            'template_path': os.path.join(settings.BASE_PATH,
                                          'web/assets/templates/'),
            'static_path': os.path.join(settings.BASE_PATH,
                                        'web/assets/static/'),
            'debug': True,
        }
        tornado.web.Application.__init__(self, handlers, **app_settings)


iloop = tornado.ioloop.IOLoop()


def run_server(host, port):
    print('Started Web GUI at {}:{}'.format(host, port))
    web_server = Application()
    web_server.listen(port, address=host)
    iloop.current().start()


def stop_server(*args, **kwargs):
    if iloop:
        iloop.current().stop()
        sys.exit(0)
