#!/usr/bin/env python3
"""Verify a Pages publication using anonymous HTTP requests and its file manifest."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import PurePosixPath
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlencode, urlsplit
from urllib.request import Request, urlopen

TEXT_TYPES = {".html": "text/html", ".css": "text/css", ".js": "javascript",
              ".json": "application/json", ".csv": "text/", ".txt": "text/"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico"}


def request(base, path, *, method="GET", byte_range=False, bust=False):
    url = base + quote(path, safe="/")
    if bust:
        url += "?" + urlencode({"pages-check": time.time_ns()})
    headers = {"User-Agent": "road-defect-research-pages-check",
               "Accept-Encoding": "identity", "Cache-Control": "no-cache"}
    if byte_range:
        headers["Range"] = "bytes=0-1023"
    # No cookies, credentials, or authenticated GitHub requests are used.
    try:
        response = urlopen(Request(url, headers=headers, method=method), timeout=30)
    except HTTPError as error:
        error.close()
        raise
    with response:
        final = urlsplit(response.geturl())
        origin = urlsplit(base)
        if (final.scheme, final.netloc) != (origin.scheme, origin.netloc):
            raise ValueError(f"{path}: redirected outside the public site")
        if not unquote(final.path).startswith(unquote(origin.path)):
            raise ValueError(f"{path}: redirected outside the project path")
        expected_status = 206 if byte_range else 200
        if response.status != expected_status:
            raise ValueError(f"{path}: HTTP {response.status}, expected {expected_status}")
        body = (response.read(1024) if byte_range else response.read()) if method != "HEAD" else b""
        return response.headers, body


def manifest_from_public_site(base, expected_revision):
    _, body = request(base, "deployment.json", bust=True)
    manifest = json.loads(body)
    if not re.fullmatch(r"[0-9a-f]{40}", manifest.get("commit", "")):
        raise ValueError("deployment.json has no valid commit")
    if expected_revision and manifest["commit"] != expected_revision:
        raise ValueError("the public site is still serving a different revision")
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError("deployment.json has no public files")
    paths = set()
    for item in files:
        path = item.get("path", "")
        parts = PurePosixPath(path).parts
        if (not path or path.startswith("/") or "\\" in path or
                ".." in parts or path != PurePosixPath(path).as_posix() or
                path in paths or not isinstance(item.get("bytes"), int) or
                item["bytes"] < 0 or not re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", ""))):
            raise ValueError("deployment.json contains an invalid or duplicate file")
        paths.add(path)
    if not {"index.html", ".nojekyll", "video.html", "map.html"}.issubset(paths):
        raise ValueError("required public entry points are missing")
    home = next(item for item in files if item["path"] == "index.html")
    headers, homepage = request(base, "", bust=True)
    if "text/html" not in headers.get("Content-Type", ""):
        raise ValueError("the public homepage is not HTML")
    if hashlib.sha256(homepage).hexdigest() != home["sha256"]:
        raise ValueError("the public homepage does not match the uploaded artifact")
    return manifest


def check_file(base, item):
    path = item["path"]
    suffix = PurePosixPath(path).suffix.lower()
    is_text = suffix in TEXT_TYPES
    is_video = suffix == ".mp4"
    last_error = None
    for attempt in range(3):
        try:
            headers, body = request(base, path, method="GET" if is_text or is_video else "HEAD",
                                    byte_range=is_video)
            content_type = headers.get("Content-Type", "").lower()
            if is_text:
                if TEXT_TYPES[suffix] not in content_type:
                    raise ValueError(f"{path}: unexpected Content-Type {content_type}")
                if hashlib.sha256(body).hexdigest() != item["sha256"]:
                    raise ValueError(f"{path}: public content differs from the artifact")
            elif is_video:
                if not content_type.startswith("video/"):
                    raise ValueError(f"{path}: video Content-Type is missing")
                if headers.get("Content-Range") != f"bytes 0-1023/{item['bytes']}":
                    raise ValueError(f"{path}: video byte-range seeking is unavailable")
                if len(body) != 1024 or body[4:8] != b"ftyp":
                    raise ValueError(f"{path}: invalid MP4 header")
            else:
                if int(headers.get("Content-Length", "-1")) != item["bytes"]:
                    raise ValueError(f"{path}: public file size differs from the artifact")
                if suffix in IMAGE_SUFFIXES and not content_type.startswith("image/"):
                    raise ValueError(f"{path}: image Content-Type is missing")
            return
        except (HTTPError, URLError, OSError, ValueError) as error:
            last_error = error
            if attempt < 2:
                time.sleep(2)
    raise ValueError(f"{path}: {last_error}")


def verify(base, expected_revision=None, attempts=18, delay=10, workers=8):
    manifest = None
    for attempt in range(attempts):
        try:
            manifest = manifest_from_public_site(base, expected_revision)
            break
        except (HTTPError, URLError, OSError, ValueError, KeyError, TypeError) as error:
            print(f"Publication readiness {attempt + 1}/{attempts}: {error}", flush=True)
            if attempt + 1 == attempts:
                raise ValueError("the anonymous public homepage/revision did not become ready") from error
            time.sleep(delay)
    errors = []
    files = manifest["files"]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = {pool.submit(check_file, base, item): item for item in files}
        for future in as_completed(results):
            try:
                future.result()
            except Exception as error:
                errors.append(str(error))
    report = {
        "status": "FAIL" if errors else "PASS",
        "url": base,
        "homepage_http_status": 200,
        "commit": manifest["commit"],
        "files_checked": len(files),
        "html_pages": sum(item["path"].endswith(".html") for item in files),
        "images": sum(PurePosixPath(item["path"]).suffix.lower() in IMAGE_SUFFIXES for item in files),
        "videos": sum(item["path"].endswith(".mp4") for item in files),
        "errors": sorted(errors),
    }
    print(json.dumps(report, indent=2), flush=True)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as stream:
            stream.write(f"### Anonymous public website verification: {report['status']}\n\n")
            stream.write(f"[Public website]({base}) — revision `{report['commit']}`\n\n")
            stream.write(f"HTTP 200 homepage; {report['files_checked']} files, "
                         f"{report['html_pages']} HTML pages, {report['images']} images, "
                         f"{report['videos']} videos checked.\n")
            for error in report["errors"][:30]:
                stream.write(f"\n- {error}")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--expected-revision")
    parser.add_argument("--attempts", type=int, default=18)
    parser.add_argument("--delay", type=float, default=10)
    args = parser.parse_args()
    url = urlsplit(args.url)
    if url.scheme != "https" or not url.netloc or url.username or url.password or url.query or url.fragment:
        parser.error("--url must be an HTTPS project URL without credentials or a query")
    if args.attempts < 1 or args.delay < 0:
        parser.error("--attempts must be positive and --delay cannot be negative")
    try:
        report = verify(args.url.rstrip("/") + "/", args.expected_revision, args.attempts, args.delay)
    except (ValueError, KeyError, TypeError) as error:
        print(f"Public site verification failed: {error}", file=sys.stderr)
        return 1
    return int(bool(report["errors"]))


if __name__ == "__main__":
    sys.exit(main())
