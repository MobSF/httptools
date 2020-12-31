#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""The Main."""
import os
import sys
import signal
import argparse

from mitmproxy import exceptions

from http_tools.modules.runner import run_module
from http_tools.web.server import (
    run_server,
    stop_server)
import http_tools.settings as settings


def init(dirs):
    signal.signal(signal.SIGTERM, stop_server)
    signal.signal(signal.SIGINT, stop_server)
    for folder in dirs:
        if not os.path.exists(folder):
            os.makedirs(folder)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-m', '--mode', help=('Supported modes\n'
                              '1. capture: Capture requests.\n'
                              '2. repeat: Repeat captured requests.\n'
                              '3. intercept: Intercept and'
                              ' tamper the request.\n'
                              '4. server: Start httptools server.\n'))
    parser.add_argument('-p', '--port', help='Proxy Port',
                        default=settings.PROXY_PORT)
    parser.add_argument('-i', '--ip', help='Proxy Host',
                        default=settings.PROXY_HOST)
    parser.add_argument('-n', '--name', help='Project Name',
                        default='default')
    parser.add_argument('-u', '--upstream', help='Upstream Proxy',
                        default=None)
    argz = parser.parse_args()
    if argz.mode:
        try:
            init([settings.FLOWS_DIR])
            if argz.mode in ['capture', 'intercept', 'repeat']:
                run_module(argz.mode,
                           argz.name,
                           argz.ip,
                           argz.port,
                           argz.upstream)
            elif argz.mode == 'server':
                run_server(argz.ip, argz.port)
            else:
                parser.print_help()
        except (KeyboardInterrupt, RuntimeError):
            pass
        except exceptions.ServerException as exp:
            print(exp)
            sys.exit(0)
        except Exception as exp:
            print('[ERROR] ' + str(exp))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
