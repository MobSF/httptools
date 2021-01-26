#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Mitmproxy runners."""
import os

from mitmproxy.tools import (
    cmdline,
    dump)
from mitmproxy.tools.main import run

import http_tools.settings as settings


def run_module(mode, project_name, host, port, upstream):
    flow_file = os.path.join(settings.FLOWS_DIR, project_name + '.flow')
    script_dir = os.path.join(settings.BASE_PATH, 'modules')
    arguments = [
        '--listen-host', host,
        '--listen-port', str(port)]
    if upstream:
        arguments.extend([
            '-k', '-m',
            'upstream:{}'.format(upstream)])
    if mode == 'capture':
        arguments.extend([
            '--scripts', os.path.join(script_dir, 'capture.py'),
            '--save-stream-file', flow_file,
            '--flow-detail', '0'])
    elif mode == 'intercept':
        arguments.extend([
            '--scripts', os.path.join(script_dir, 'interceptor.py')])
    elif mode == 'repeat':
        arguments = [
            '-n',
            '--client-replay', flow_file]
        if upstream:
            arguments.extend([
                '-k', '-m',
                'upstream:{}'.format(upstream)])
    run(dump.DumpMaster, cmdline.mitmdump, arguments, {})
