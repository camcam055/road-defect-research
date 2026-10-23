#!/usr/bin/env python3
"""Verify actual gallery JPEGs, metadata removal, dimensions and visible box pixels."""
from pathlib import Path
import json
from PIL import Image
from gallery_checks import check_gallery

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "site/assets/gallery"

def border_pixels(image, regions):
    width, height = image.size
    pixels = image.load()
    coloured, sampled = 0, 0
    for box in regions:
        a, b, c, d = [round(value * (width if i % 2 == 0 else height)) for i, value in enumerate(box)]
        for y in range(max(0, b - 3), min(height, d + 4)):
            for x in range(max(0, a - 3), min(width, c + 4)):
                if min(abs(x-a), abs(x-c), abs(y-b), abs(y-d)) <= 3:
                    red, green, blue = pixels[x, y]
                    sampled += 1
                    if blue > 100 and blue-red > 35 and (blue-green > 30 or green-red > 40):
                        coloured += 1
    return coloured, coloured / max(sampled, 1)

def verify():
    data = json.loads((ROOT / "site/data/gallery.json").read_text())
    errors = check_gallery(data, ASSETS)
    checked = 0
    for row in data["images"]:
        for mode in ("after", "before"):
            if not row.get(mode):
                continue
            with Image.open(ASSETS / row[mode]) as image:
                image.load()
                if image.format != "JPEG" or image.size != (row["display_width"], row["display_height"]):
                    errors.append("Image format/dimensions do not match: " + row[mode])
                if image.getexif():
                    errors.append("Unexpected EXIF metadata: " + row[mode])
                if mode == "after":
                    coloured, ratio = border_pixels(image.convert("RGB"), row["review"]["box_regions"])
                    if coloured < 30 or ratio < 0.02:
                        errors.append("Visible coloured box evidence missing: " + row["id"])
                checked += 1
    report = {"status": "FAIL" if errors else "PASS", "annotated_photos": len(data["images"]),
              "jpeg_files_checked": checked, "errors": errors}
    print(json.dumps(report, indent=2))
    return bool(errors)

if __name__ == "__main__":
    raise SystemExit(verify())
