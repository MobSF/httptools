#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Dump HTTP Traffic."""
import sys

from mitmproxy import (
    ctx,
    http,
)


class HTTPDump:

    def __init__(self):
        self.http_dump_file = ctx.options.save_stream_file + '.txt'
        self.http_f = open(self.http_dump_file, 'w')

    def save_http(self, httpflow):
        """Dump HTTP Request and Response."""
        self.http_f.write('========\n')
        self.http_f.write('REQUEST\n')
        self.http_f.write('========\n')
        req = httpflow.request
        res = httpflow.response
        self.http_f.write('%s %s %s\n' %
                          (req.method, req.url, req.http_version))
        for key, val in req.headers.items():
            self.http_f.write('%s: %s\n' % (key, val))
        if req.content:
            self.http_f.write('\n\n%s\n' %
                              (req.content))

        self.http_f.write('=========\n')
        self.http_f.write('RESPONSE\n')
        self.http_f.write('=========\n')
        self.http_f.write('%s %s %s\n' %
                          (res.http_version, res.status_code, res.reason))
        for key, val in res.headers.items():
            self.http_f.write('%s: %s\n' % (key, val))
        if res.content:
            self.http_f.write('\n\n%s\n' %
                              (res.content))

    def done(self):
        if self.http_f:
            self.http_f.close()

    def request(self, flow: http.HTTPFlow) -> None:
        """Kill Proxy on Kll Request."""
        for key, val in flow.request.headers.items():
            if 'httptools' in key and val == 'kill':
                sys.exit(0)

    def response(self, flow: http.HTTPFlow) -> None:
        if self.http_f:
            self.save_http(flow)


addons = [HTTPDump()]
