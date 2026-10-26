#!/usr/bin/env python3
"""Verify gallery JPEG/PNG files, dimensions, metadata and visible box pixels."""
from pathlib import Path
import json
from PIL import Image
from gallery_checks import check_gallery

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "site/assets/gallery"

def border_pixels(image, regions, original=None):
    width, height = image.size
    pixels = image.load()
    reference = original.load() if original is not None and original.size == image.size else None
    coloured, sampled = 0, 0
    for box in regions:
        a, b, c, d = [round(value * (width if i % 2 == 0 else height)) for i, value in enumerate(box)]
        for y in range(max(0, b - 3), min(height, d + 4)):
            for x in range(max(0, a - 3), min(width, c + 4)):
                if min(abs(x-a), abs(x-c), abs(y-b), abs(y-d)) <= 3:
                    red, green, blue = pixels[x, y]
                    sampled += 1
                    blue_border = blue > 100 and blue-red > 35 and (blue-green > 30 or green-red > 40)
                    # Some saved YOLO classes use white boxes. Require a change
                    # from the matching original so road paint cannot pass alone.
                    white_border = (reference is not None and min(red, green, blue) >= 220
                                    and max(red, green, blue) - min(red, green, blue) < 30
                                    and max(abs(a-b) for a, b in zip((red, green, blue), reference[x, y])) >= 40)
                    if blue_border or white_border:
                        coloured += 1
    return coloured, coloured / max(sampled, 1)

def verify():
    data = json.loads((ROOT / "site/data/gallery.json").read_text())
    errors = check_gallery(data, ASSETS)
    checked = 0
    formats = {"JPEG": 0, "PNG": 0}
    for row in data["images"]:
        original = None
        if row.get("before"):
            with Image.open(ASSETS / row["before"]) as before:
                original = before.convert("RGB")
        for mode in ("after", "before"):
            if not row.get(mode):
                continue
            with Image.open(ASSETS / row[mode]) as image:
                image.load()
                expected_format = {".jpg": "JPEG", ".png": "PNG"}.get(Path(row[mode]).suffix.lower())
                if image.format != expected_format or image.size != (row["display_width"], row["display_height"]):
                    errors.append("Image format/dimensions do not match: " + row[mode])
                if image.getexif():
                    errors.append("Unexpected EXIF metadata: " + row[mode])
                if mode == "after":
                    coloured, ratio = border_pixels(image.convert("RGB"), row["review"]["box_regions"], original)
                    if coloured < 30 or ratio < 0.02:
                        errors.append("Visible annotation border evidence missing: " + row["id"])
                checked += 1
                formats[image.format] = formats.get(image.format, 0) + 1
    report = {"status": "FAIL" if errors else "PASS", "annotated_photos": len(data["images"]),
              "image_files_checked": checked, "jpeg_files_checked": formats["JPEG"],
              "png_files_checked": formats["PNG"], "errors": errors}
    print(json.dumps(report, indent=2))
    return bool(errors)

if __name__ == "__main__":
    raise SystemExit(verify())
