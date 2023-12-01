## Setup

```
git clone https://github.com/MobSF/httptools.git
cd httptools
git checkout rd
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Running

### Intercept Fuzzable GQL queries

Intercept mode will run an HTTPS proxy on `0.0.0.0:1337` and uses `http_tools/modules/interceptor.py`. This script will capture and parse GraphQL requests that has a user input variable. These are the requests we want to fuzz for IDOR.

`httptools -m intercept`

After running the above, point your browser or mobile app traffic to '127.0.0.1:1337'. Jailbroken iOS in Corellium doesn't need Root CA install. Also you can use Burp's Chromium browser with an addon like [FoxyPoxy](https://chrome.google.com/webstore/detail/foxyproxy-standard/gcknhkkoolaabfmlnjonogaaifnjlfnp) to redirect the traffic to the proxy without any Root CA install, otherwise CA files are present in `~/.mitmproxy`

Kill the proxy process to stop capturing traffic.


### View Captured GQL requests

This is optional, but if you want to view the GraphQL request that you just captured.

`httptools -m server`

You can see the captured HTTP request/response pair in the web UI: http://127.0.0.1:1337/


### Fuzz for Horizontal IDOR

The IDOR fuzzing logic is available in `http_tools/modules/fuzzer.py`. The script loads the captured request and replaces authtoken/cookies that belong to a different user, repeat the request and compare the response with the original response. If they match then that's a possible IDOR.

Modify the file `http_tools/modules/fuzzer.py`, at line no 100, Set the authtoken or cookies value in the `modified` variable.

Run the fuzzer.

`httptools -m fuzzer`