#!/usr/bin/env python3
"""Exercise false-success cases against a local anonymous HTTP server."""
from contextlib import redirect_stdout
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import threading
import unittest
from unittest.mock import patch

from verify_public_site import verify

REVISION = "a" * 40


class PublicSiteTests(unittest.TestCase):
    def setUp(self):
        self.files = {
            "index.html": b"<html>Research homepage</html>",
            ".nojekyll": b"",
            "map.html": b"<html>Map</html>",
            "video.html": b"<html>Videos</html>",
            "photo.jpg": b"published-image-bytes",
            "demo.mp4": b"\x00\x00\x00\x20ftyp" + b"0" * 2040,
        }
        self.mode = "healthy"
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_HEAD(self):
                self.respond(True)

            def do_GET(self):
                self.respond(False)

            def respond(self, head):
                path = self.path.split("?", 1)[0]
                if path == "/login":
                    self.send_response(200)
                    self.end_headers()
                    return
                key = path.removeprefix("/project/") or "index.html"
                if key == "deployment.json":
                    body = json.dumps({
                        "commit": REVISION,
                        "files": [{"path": name, "bytes": len(content),
                                   "sha256": hashlib.sha256(content).hexdigest()}
                                  for name, content in owner.files.items()],
                    }).encode()
                    content_type = "application/json"
                elif key in owner.files:
                    body = owner.files[key]
                    content_type = ("text/html" if key.endswith(".html") else
                                    "video/mp4" if key.endswith(".mp4") else
                                    "image/jpeg" if key.endswith(".jpg") else
                                    "application/octet-stream")
                else:
                    self.send_error(404)
                    return
                if owner.mode == "404" and key == "index.html":
                    self.send_error(404)
                    return
                if owner.mode == "login" and key == "photo.jpg":
                    self.send_response(302)
                    self.send_header("Location", "/login")
                    self.end_headers()
                    return
                if owner.mode == "missing-image" and key == "photo.jpg":
                    self.send_error(404)
                    return
                if owner.mode == "wrong-home" and key == "index.html":
                    body = b"<html>Site not found</html>"
                if owner.mode == "stale-page" and key == "map.html":
                    body = b"<html>Old map page</html>"
                if owner.mode == "truncated-image" and key == "photo.jpg":
                    body = body[:-1]
                partial = bool(self.headers.get("Range")) and owner.mode != "no-range"
                self.send_response(206 if partial else 200)
                self.send_header("Content-Type", content_type)
                if partial:
                    self.send_header("Content-Range", f"bytes 0-1023/{len(body)}")
                    body = body[:1024]
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if not head:
                    self.wfile.write(body)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}/project/"
        self.output = redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.sleeps = patch("verify_public_site.time.sleep")
        self.sleeps.start()
        self.summary = patch.dict("os.environ", {"GITHUB_STEP_SUMMARY": ""})
        self.summary.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.summary.stop()
        self.sleeps.stop()
        self.output.__exit__(None, None, None)

    def check(self, revision=REVISION):
        return verify(self.base, revision, attempts=1, delay=0, workers=2)

    def test_valid_anonymous_site_and_video_ranges(self):
        result = self.check()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["files_checked"], 6)
        self.assertEqual(result["videos"], 1)

    def test_site_not_found_is_a_failure(self):
        self.mode = "404"
        with self.assertRaises(ValueError):
            self.check()

    def test_http_200_error_page_is_a_failure(self):
        self.mode = "wrong-home"
        with self.assertRaises(ValueError):
            self.check()

    def test_old_revision_is_a_failure(self):
        with self.assertRaises(ValueError):
            self.check("b" * 40)

    def test_stale_page_is_a_failure(self):
        self.mode = "stale-page"
        self.assertEqual(self.check()["status"], "FAIL")

    def test_missing_image_is_a_failure(self):
        self.mode = "missing-image"
        self.assertEqual(self.check()["status"], "FAIL")

    def test_truncated_image_is_a_failure(self):
        self.mode = "truncated-image"
        self.assertEqual(self.check()["status"], "FAIL")

    def test_video_without_seeking_is_a_failure(self):
        self.mode = "no-range"
        self.assertEqual(self.check()["status"], "FAIL")

    def test_login_redirect_is_a_failure(self):
        self.mode = "login"
        self.assertEqual(self.check()["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
