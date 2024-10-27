"""Upstream proxy module."""

import http_tools.settings as settings

from mitmproxy import ctx
from mitmproxy import http
from mitmproxy.connection import Server
from mitmproxy.net.server_spec import ServerSpec


def load(loader):
    loader.add_option(
        name='proxy_ip',
        typespec=str,
        default='127.0.0.1',
        help='Upstream Proxy IP',
    )
    loader.add_option(
        name='proxy_port',
        typespec=int,
        default=8000,
        help='Upstream Proxy Port',
    )


def request(flow: http.HTTPFlow) -> None:
    if (flow.request.url.endswith('/kill')
            and flow.request.method == 'GET'
            and flow.request.port == settings.PROXY_PORT):
        # Prevent killing the proxy server
        flow.kill()

    address = (ctx.options.proxy_ip, ctx.options.proxy_port)
    # Check if the server connection already exists
    if flow.server_conn.timestamp_start:
        # Replace the existing server connection with a new one
        flow.server_conn = Server(address=flow.server_conn.address)

    # Set the upstream proxy (via) server
    flow.server_conn.via = ServerSpec(('http', address))
