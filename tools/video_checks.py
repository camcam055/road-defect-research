"""Standard-library checks for the final, GitHub Pages-compatible video sequence."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import struct

EXPECTED_SOURCES = ["Data Collection Video new.mov", "Training the AI new.mov", "From Road to Results.mov"]
EXPECTED_TITLES = ["Data Collection", "AI Training", "Road Defect Detection"]

class VideoPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.players, self.stages, self.elements = [], [], {}
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "video":
            self.players.append(data)
        if "data-video-stage" in data:
            self.stages.append(data)
        if "id" in data:
            self.elements[data["id"]] = data

def mp4_boxes(path):
    boxes = []
    with path.open("rb") as stream:
        length = path.stat().st_size
        while stream.tell() < length:
            start = stream.tell()
            header = stream.read(8)
            if len(header) < 8:
                raise ValueError("Incomplete MP4 box")
            size, kind = struct.unpack(">I4s", header)
            header_size = 8
            if size == 1:
                size = struct.unpack(">Q", stream.read(8))[0]
                header_size = 16
            if size == 0:
                size = length - start
            if size < header_size or start + size > length:
                raise ValueError("Invalid MP4 box length")
            payload = stream.read(size - header_size) if kind == b"moov" else b""
            boxes.append((kind, payload))
            stream.seek(start + size)
    return boxes

def check_video_site(site):
    errors = []
    try:
        data = json.loads((site / "data/videos.json").read_text())
        videos = data["videos"]
        if [row["source_file"] for row in videos] != EXPECTED_SOURCES:
            errors.append("Final video source order changed")
        if [row["title"] for row in videos] != EXPECTED_TITLES:
            errors.append("Final video stage labels changed")
        page = VideoPage()
        page.feed((site / "video.html").read_text())
        if len(page.players) != 1:
            errors.append("Project video must use exactly one player")
        else:
            player = page.players[0]
            if not all(key in player for key in ("controls", "playsinline")) or any(key in player for key in ("autoplay", "loop")):
                errors.append("Project video native controls or playback behavior changed")
            if "nodownload" not in player.get("controlslist", "").split():
                errors.append("Native video download control must be hidden")
            if player.get("src") != videos[0]["src"] or player.get("poster") != videos[0]["poster"]:
                errors.append("Initial player does not use the first final video")
        if len(page.stages) != 3:
            errors.append("Three manual video stage buttons are required")
        else:
            for index, (stage, row) in enumerate(zip(page.stages, videos)):
                if stage.get("data-video-stage") != str(index) or stage.get("data-src") != row["src"] or stage.get("data-title") != row["title"] or stage.get("data-poster") != row["poster"]:
                    errors.append("Video stage buttons do not match final assets")
        for name in ("video-status", "video-error", "video-retry"):
            if name not in page.elements:
                errors.append(f"Project video control missing: {name}")
        if any(name in page.elements for name in ("video-next", "video-previous")):
            errors.append("Removed Previous/Next video controls reappeared")
        if page.elements.get("video-map", {}).get("href") != "map.html":
            errors.append("Final video map link must target the existing map")
        for row in videos:
            if len(row.get("source_sha256", "")) != 64 or row["duration_seconds"] <= 0:
                errors.append("Video source provenance is incomplete")
            for key in ("src", "poster"):
                ref = row[key]
                path = (site / ref).resolve()
                if not ref.startswith("assets/video/") or not path.is_relative_to((site / "assets/video").resolve()) or not path.is_file():
                    errors.append(f"Unavailable or unsafe video asset: {ref}")
                    continue
                if key != "src":
                    continue
                if path.suffix != ".mp4" or path.stat().st_size >= 100 * 1024 * 1024:
                    errors.append(f"Video is not a GitHub-compatible MP4: {ref}")
                if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"] or path.stat().st_size != row["bytes"]:
                    errors.append(f"Final video checksum or size changed: {ref}")
                boxes = mp4_boxes(path)
                kinds = [kind for kind, _ in boxes]
                if b"moov" not in kinds or b"mdat" not in kinds or kinds.index(b"moov") > kinds.index(b"mdat"):
                    errors.append(f"MP4 fast-start metadata missing: {ref}")
                moov = next((payload for kind, payload in boxes if kind == b"moov"), b"")
                if b"avc1" not in moov:
                    errors.append(f"Expected H.264 encoding missing: {ref}")
                if row.get("audio") is not False or b"mp4a" in moov:
                    errors.append(f"Silent video should have no audio stream: {ref}")
    except (OSError, ValueError, KeyError, TypeError, struct.error) as exc:
        errors.append(f"Project video validation failed: {exc}")
    return errors
