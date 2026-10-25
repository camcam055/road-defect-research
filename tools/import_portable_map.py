#!/usr/bin/env python3
"""Import a portable Folium export while keeping source audits outside the repository."""
import argparse
import csv
import hashlib
import io
import json
import re
import shutil
from pathlib import Path, PurePosixPath
from datetime import datetime
from zoneinfo import ZoneInfo
from extract_report import clean_image
from layout import SITE

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.audit.resolve().is_relative_to(SITE.parent.resolve()):
        raise SystemExit("Source audit must remain outside the repository")
    source = args.source.read_text()
    prefix = args.source.stem + "_assets/"
    asset_root = args.source.parent / prefix
    if not asset_root.is_dir() or prefix not in source:
        raise SystemExit("The HTML and its portable assets folder must stay together")
    if "file://" in source or "/Users/" in source:
        raise SystemExit("Review private paths in the source map before importing")
    output = SITE / "assets/map"
    output.mkdir(parents=True, exist_ok=True)
    args.audit.mkdir(parents=True, exist_ok=True)
    observations = (asset_root / "observations.csv").read_text()
    reader = csv.DictReader(io.StringIO(observations))
    rows = list(reader)
    references = set(re.findall(re.escape(prefix) + r'([^"\\\s<>\x60]+)', source))
    references.update(row["image_url"][len(prefix):] for row in rows if row["image_url"].startswith(prefix))
    images = sorted(path for path in references if path.startswith("images/"))
    if not images:
        raise SystemExit("No portable map images found")
    for relative in images:
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or not (asset_root / relative).is_file():
            raise SystemExit("A referenced image is missing or outside the portable assets")
    # These historical photographs were withheld in the preceding publication.
    # They are absent from the revised export; reject accidental reintroduction.
    withheld_sources = {"run12/frame_0038.jpg", "run12/frame_0060.jpg", "run12/frame_0067.jpg"}
    manifest = json.loads((asset_root / "image_manifest.json").read_text())
    if any(row["source"] in withheld_sources and row["file"] in images for row in manifest):
        raise SystemExit("Previously withheld photographs need an explicit privacy review")
    records = []
    for n, relative in enumerate(images, 1):
        raw = (asset_root / relative).read_bytes()
        cleaned = clean_image(raw, Path(relative).suffix)
        dest = output / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(cleaned)
        records.append({"file": relative, "source_sha256": digest(raw), "public_sha256": digest(cleaned)})
        if n % 400 == 0:
            print(f"Verified {n}/{len(images)} map photographs", flush=True)
    # Retain the export's bundled versions and licences, plus existing icon fallbacks.
    for path in (asset_root / "vendor").rglob("*"):
        if path.is_file():
            dest = output / "vendor" / path.relative_to(asset_root / "vendor")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
    (output / "observations.csv").write_text(observations.replace(prefix, ""))
    canonical = source.replace(prefix, "")
    head = '<title>Road defect research map</title><link rel="stylesheet" href="map-adapter.css">'
    tail = '<script src="map-adapter.js" defer></script>'
    public = canonical.replace("</head>", head + "</head>", 1)
    public = public.replace("</html>", tail + "</html>", 1)
    if public.replace(head, "", 1).replace(tail, "", 1) != canonical:
        raise SystemExit("Unexpected map change")
    (output / "index.html").write_text(public)
    # A private snapshot is created by the update workflow before this importer.
    # Remove obsolete public copies that the current export no longer references.
    old_photos = output / "photos"
    if old_photos.exists():
        shutil.rmtree(old_photos)
    for path in (output / "images").iterdir():
        if path.is_file() and "images/" + path.name not in images:
            path.unlink()
    located = sum(bool(row["lat"] and row["lon"]) for row in rows)
    summary = {
        "source": "Latest supplied portable road defect map",
        "source_saved": datetime.fromtimestamp(args.source.stat().st_mtime, ZoneInfo("Pacific/Auckland")).strftime("%d %B %Y").lstrip("0"),
        "source_sha256": digest(source.encode()),
        "public_sha256": digest(public.encode()),
        "verification": "Entire map matches the source after relative asset paths, a page title and the separate website navigation adapter. Geographic features, grouped observations, density values, labels and qualifications are unchanged.",
        "marker_count": source.count("L.marker("),
        "tentative_defect_locations": len({row["group_id"] for row in rows if row["lat"] and row["lon"]}),
        "located_observations": located,
        "observations_without_gps": len(rows) - located,
        "all_observations_csv_rows": len(rows),
        "map_photographs": len(images),
        "qualifications": [
            "Grouping is conservative and provisional; GPS marks the camera position.",
            "Recovered run16 section density is shown separately from the existing latest-inspection assessment.",
            "Grey density sections are not assessable.",
            "Mapped detections and visual observations do not establish measured accuracy."
        ]
    }
    (SITE / "data/map-source.json").write_text(json.dumps(summary, indent=2) + "\n")
    (args.audit / "map-audit.json").write_text(json.dumps({**summary, "assets": records}, indent=2) + "\n")
    print(json.dumps({"status": "PASS", **{k: summary[k] for k in ("marker_count", "tentative_defect_locations", "located_observations", "observations_without_gps", "map_photographs")}}, indent=2))

if __name__ == "__main__":
    main()
