#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Web Dashboard Functions."""
import os
import glob
from pathlib import PurePath
from urllib.parse import urlparse
import subprocess
import threading

import tornado
import tornado.web

from http_tools.web.flow_tools import (
    get_flow_file,
    get_flow_meta,
    get_sorted_flows,
    load_flows,
)
import http_tools.settings as settings


class DashboardHandler(tornado.web.RequestHandler):

    def get(self, project='default'):
        flow_file = get_flow_file(project)
        if not flow_file:
            self.write('[ERROR] No requests found for the project')
            return
        flows = load_flows(flow_file)
        sorted_flows = get_sorted_flows(flows)
        projects = []
        flow_files = glob.glob(
            settings.FLOWS_DIR + '**/*.flow',
            recursive=True)
        projects = [PurePath(f).stem for f in flow_files]
        context = {'title': 'MobSF- HTTPTools',
                   'project': project,
                   'projects': projects,
                   'sorted_flows': sorted_flows}
        self.render('dashboard.html', **context)


class FlowMetaHandler(tornado.web.RequestHandler):

    def post(self):
        try:
            flow_id = self.request.headers.get('X-Flow-ID', '')
            project = self.get_argument('project', default='')
            flow_file = get_flow_file(project)
            if not flow_id or not flow_file:
                self.write({'id': ''})
                return
            flows = load_flows(flow_file)
            for flow in flows:
                if flow.id == flow_id:
                    self.write(get_flow_meta(flow))
        except Exception as exp:
            print('[ERROR] ', str(exp))
            self.write({'error': str(exp)})


class RepeatHandler(tornado.web.RequestHandler):

    def post(self, project):
        flow_file = get_flow_file(project)
        if not flow_file:
            self.write({'error': 'No requests found for the project'})
            return
        proxy = self.get_argument('proxy', default='http://127.0.0.1:8080')
        parsed_url = urlparse(proxy)
        flow_file = os.path.join(settings.FLOWS_DIR, project + '.flow')
        script_dir = os.path.join(settings.BASE_PATH, 'modules')
        # mitmproxy 11.0.0 has issues with client replay and upstream proxy
        # See: https://github.com/mitmproxy/mitmproxy/issues/7280
        args = ['mitmdump',
                '--scripts', os.path.join(script_dir, 'upstream.py'),
                '--set', 'connection_strategy=lazy',
                '--set', 'upstream_cert=false',
                '--set', f'proxy_ip={parsed_url.hostname}',
                '--set', f'proxy_port={parsed_url.port}',
                '--ssl-insecure',
                '--no-server',
                '--client-replay', flow_file]
        trd = threading.Thread(target=subprocess.call, args=(args,))
        trd.setDaemon(True)
        trd.start()
        self.write({'success': 'Repeating request to upstream'})
