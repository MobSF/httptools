#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Utils for flows."""
import os
import urllib.parse

from mitmproxy import io
from mitmproxy.http import HTTPFlow

import http_tools.settings as settings


def get_flow_file(flow_name):
    """Get Flow File Safetly."""
    flow_name = flow_name + '.flow'
    flow_dir = settings.FLOWS_DIR
    requested_path = os.path.join(flow_dir, flow_name)
    pfx = os.path.commonprefix((os.path.realpath(requested_path), flow_dir))
    if pfx == flow_dir and os.path.exists(requested_path):
        return requested_path
    return False


def get_headers(headers):
    """By default headers are folded by mitmproxy."""
    headers_dict = {}
    for key, val in headers.items():
        headers_dict[key] = val
    return headers_dict


def get_flow_meta(flow):
    flow_meta = {}
    flow_meta['id'] = flow.id
    # Request
    content = flow.request.content.decode(
        'utf-8', 'ignore') if flow.request.content else ''
    request_headers = get_headers(flow.request.headers)
    flow_meta['request'] = {
        'method': flow.request.method,
        'url': flow.request.url,
        'http_version': flow.request.http_version,
        'headers': request_headers,
        'content': content,
    }
    # Response
    response_headers = get_headers(flow.response.headers)
    res_content = flow.response.content.decode(
        'utf-8', 'ignore') if flow.response.content else ''
    flow_meta['response'] = {
        'http_version': flow.response.http_version,
        'status_code': flow.response.status_code,
        'reason': flow.response.reason,
        'headers': response_headers,
        'content': res_content,
    }
    return flow_meta


def get_protocol_domain(url, trailing=True):
    try:
        parsed_uri = urllib.parse.urlparse(url)
        if trailing:
            return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    except Exception as exp:
        print('[ERROR] Parsing Protocol and Domain - %s' % exp)


def load_flows(path):
    flows = []
    with open(path, 'rb') as f:
        flows.extend(io.FlowReader(f).stream())
    return flows


def get_sorted_flows(flows):
    # Add URL under domains
    sorted_flows = {}
    for flow in flows:
        if not isinstance(flow, HTTPFlow):
            continue
        domain = get_protocol_domain(flow.request.url, False)
        meta = {'id': flow.id, 'method': flow.request.method,
                'relative': flow.request.url.replace(domain, '', 1),
                'url': flow.request.url}
        if domain in sorted_flows:
            sorted_flows[domain].append(meta)
        else:
            sorted_flows[domain] = [meta]
    return sorted_flows
