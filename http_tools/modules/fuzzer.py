"""IDOR Fuzzer."""
import json
import hashlib
from pathlib import Path

from mitmproxy import (
    ctx,
    http,
    io,
)
import mitmproxy.addonmanager
import mitmproxy.http
import mitmproxy.log
import mitmproxy.tcp
from mitmproxy.exceptions import FlowReadException

import http_tools.settings as settings
from http_tools.utils import (
    C,
    dict_generator,
)


JSON_RESPONSES = {}


class ResponseMather:
    """Intercept Web Traffic."""

    def __init__(self):
        print('IDOR Fuzzer Module Loaded')

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """HTTP Response.

        The full HTTP response has been read.
        """
        try:
            req = flow.request.get_text()
            res = flow.response.get_text()
            oldf = JSON_RESPONSES[get_md5(req)]
            if get_md5(oldf.response.get_text()) == get_md5(res):
                print(f'{C.BOLD}{C.FAIL}IDOR DETECTED!!{C.ENDC}')
                print(f'\n{C.BOLD}{C.OKCYAN}REQUEST BODY{C.ENDC}{C.OKCYAN}')
                print(json.dumps(json.loads(req), indent=2))
                print(f'{C.ENDC}{C.BOLD}{C.FAIL}\n'
                      f'RESPONSE BODY{C.ENDC}{C.FAIL}')
                print(json.dumps(json.loads(res), indent=2))
                print(C.ENDC)
        except Exception as e:
            print(f'Response Exception {str(e)}')


def get_md5(data):
    return hashlib.md5(data.encode()).hexdigest()


def repeat(f, modified):
    # Copy, modify and fuzz request
    newf = f.copy()
    if 'app' in newf.request.url:
        newf.request.headers['Cookie'] = modified
    elif 'api' in newf.request.url:
        newf.request.headers['Auth-Token'] = modified
    ctx.master.commands.call('replay.client', [newf])


def fuzz(modified):
    path = Path(settings.FLOWS_DIR) / 'default.flow'
    with path.open(mode='rb') as logfile:
        freader = io.FlowReader(logfile)
        try:
            for f in freader.stream():
                if not isinstance(f, http.HTTPFlow):
                    return
                if f.is_replay == 'request':
                    return
                if f.response.status_code != 200:
                    # Only use request with 200 OK response
                    return
                request_data = json.loads(f.request.get_text())
                fuzzable = False
                for lst in dict_generator(request_data['variables']):
                    # Fuzz only GQL queries with
                    # input variables of type str, int
                    if "<class 'str'>" in lst or "<class 'int'>" in lst:
                        fuzzable = True
                        break
                if not fuzzable:
                    # Don't fuzz boolean user inputs
                    return
                key = get_md5(f.request.get_text())
                JSON_RESPONSES[key] = f
                repeat(f, modified)
        except FlowReadException as e:
            print(f'Flow file corrupted: {e}')


addons = [ResponseMather()]
modified = '' 
# Fuzz with a different user's cookie or authtoken
fuzz(modified)
