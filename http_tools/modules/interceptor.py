#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Intercept HTTP, TCP, Websocket."""
import json
import typing
from pathlib import Path

from graphql.parser import GraphQLParser

import mitmproxy.addonmanager
import mitmproxy.http
import mitmproxy.log
import mitmproxy.tcp
from mitmproxy import io

import http_tools.settings as settings
from http_tools.utils import (
    C,
    dict_generator,
)


class Interceptor:
    """Intercept Web TraffiC."""

    def __init__(self):
        print('Interceptor Module Loaded')
        path = Path(settings.FLOWS_DIR) / 'default.flow'
        self.f: typing.BinaryIO = open(path, 'wb')
        self.w = io.FlowWriter(self.f)

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """HTTP Response.

        The full HTTP response has been read.
        """
        if flow.request.url.endswith('/graphql'):
            parser = GraphQLParser()
            try:
                request_data = json.loads(flow.request.get_text())
                if (len(request_data.get('variables'))) > 0:
                    print(f'{C.BOLD}{C.HEADER}\n\nThe GraphQL request '
                          f'contains input variables{C.ENDC}{C.WARNING}')
                    print(json.dumps(request_data, indent=2))
                    print(f'{C.ENDC}')
                    print(f'{C.BOLD}{C.OKGREEN}\nParsed Variable Types\n'
                          f'{C.ENDC}{C.OKGREEN}')
                    for i in dict_generator(request_data['variables']):
                        print(i)
                    print(f'{C.ENDC}')
                    ast = parser.parse(request_data['query'])
                    print(f'\n{C.OKBLUE}{C.BOLD}Parsed GQL AST:{C.ENDC}'
                          f'{C.OKBLUE}\n{ast}{C.ENDC}')
                    res = json.loads(flow.response.get_text())
                    print(f'{C.OKCYAN}{C.BOLD}\nResponse:{C.ENDC}{C.OKCYAN}\n'
                          f'{json.dumps(res, indent=2)}\n\n{C.ENDC}')
                    self.w.add(flow)
            except Exception as e:
                print(f'GQL Parse Exception {str(e)}')

    def done(self):
        """Done.

        Called when the addon shuts down, either by being removed from
        the mitmproxy instance, or when mitmproxy itself shuts down. On
        shutdown, this event is called after the event loop is
        terminated, guaranteeing that it will be the final event an addon
        sees. Note that log handlers are shut down at this point, so
        calls to log functions will produce no output.
        """
        self.f.close()


addons = [Interceptor()]
