#!/usr/bin/env python3
"""Serve only the public site, bound to this computer."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import argparse,webbrowser
p=argparse.ArgumentParser();p.add_argument("--port",type=int,default=8766);p.add_argument("--no-open",action="store_true");a=p.parse_args()
root=Path(__file__).resolve().parent.parent/"site"
class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control","no-store")
        super().end_headers()
server=None
for port in range(a.port,a.port+20):
    try:server=ThreadingHTTPServer(("127.0.0.1",port),partial(PreviewHandler,directory=str(root)));break
    except OSError:continue
if server is None:raise SystemExit("No available local preview port")
url=f"http://127.0.0.1:{server.server_port}/"
print(f"Local preview: {url}\nPress Control+C to stop. The website is not public.",flush=True)
if not a.no_open:webbrowser.open(url)
try:server.serve_forever()
except KeyboardInterrupt:pass
finally:server.server_close()
