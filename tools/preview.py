#!/usr/bin/env python3
"""Serve only the public site, bound to this computer."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import argparse,re,webbrowser
p=argparse.ArgumentParser();p.add_argument("--port",type=int,default=8766);p.add_argument("--no-open",action="store_true");a=p.parse_args()
root=Path(__file__).resolve().parent.parent/"site"
class PreviewHandler(SimpleHTTPRequestHandler):
    """Support native video seeking while serving only the local public site."""
    def end_headers(self):
        self.send_header("Cache-Control","no-store")
        self.send_header("Accept-Ranges","bytes")
        super().end_headers()

    def send_head(self):
        self._range_remaining=None
        requested=self.headers.get("Range")
        path=Path(self.translate_path(self.path))
        if not requested or not path.is_file():
            return super().send_head()
        match=re.fullmatch(r"bytes=(\d*)-(\d*)",requested.strip())
        size=path.stat().st_size
        if not match or not any(match.groups()) or size==0:
            return self.invalid_range(size)
        start_text,end_text=match.groups()
        if start_text:
            start=int(start_text)
            end=min(int(end_text),size-1) if end_text else size-1
        else:
            suffix=int(end_text)
            if suffix==0:
                return self.invalid_range(size)
            start=max(0,size-suffix)
            end=size-1
        if start>=size or end<start:
            return self.invalid_range(size)
        try:
            stream=path.open("rb")
        except OSError:
            self.send_error(404,"File not found")
            return None
        stream.seek(start)
        self._range_remaining=end-start+1
        self.send_response(206)
        self.send_header("Content-Type",self.guess_type(str(path)))
        self.send_header("Content-Length",str(self._range_remaining))
        self.send_header("Content-Range",f"bytes {start}-{end}/{size}")
        self.send_header("Last-Modified",self.date_time_string(path.stat().st_mtime))
        self.end_headers()
        return stream

    def invalid_range(self,size):
        self.send_response(416)
        self.send_header("Content-Range",f"bytes */{size}")
        self.send_header("Content-Length","0")
        self.end_headers()
        return None

    def copyfile(self,source,outputfile):
        if self._range_remaining is None:
            return super().copyfile(source,outputfile)
        remaining=self._range_remaining
        while remaining:
            chunk=source.read(min(64*1024,remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining-=len(chunk)
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
