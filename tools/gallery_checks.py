"""Standard-library checks for the curated gallery contract and deployed files."""
from pathlib import PurePosixPath
import hashlib
import json
import math
import re

CLASS_CATEGORY = {
    "long_crack": "longitudinal-cracks", "lateral_crack": "transverse-cracks",
    "alligator_crack": "alligator-cracking", "pothole": "potholes",
    "other_corruption": "other-surface-defects",
}

def valid_box(box):
    return (isinstance(box, list) and len(box) == 4
            and all(isinstance(x, (int, float)) and math.isfinite(x) for x in box)
            and 0 <= box[0] < box[2] <= 1 and 0 <= box[1] < box[3] <= 1)

def check_gallery(data, assets):
    errors = []
    if data.get("schema_version") != 2 or data.get("default_view") != "after":
        errors.append("Gallery must use reviewed schema 2 and default to AFTER.")
    images = data.get("images", [])
    categories = [row["id"] for row in data.get("categories", [])]
    if not images or not categories or len(categories) != len(set(categories)):
        errors.append("Gallery images/categories are empty or duplicated.")
    ids, after_hashes, original_hashes, referenced = set(), set(), set(), set()
    for row in images:
        ident = row.get("id", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", ident) or ident in ids:
            errors.append("Invalid or duplicate gallery ID: " + ident)
        ids.add(ident)
        category = row.get("category")
        if category not in categories:
            errors.append("Unknown gallery category: " + ident)
        review = row.get("review", {})
        if review.get("visible_box") is not True or review.get("reviewed") is not True:
            errors.append("Visible-box review incomplete: " + ident)
        regions = review.get("box_regions", [])
        if not regions or not all(valid_box(box) for box in regions):
            errors.append("Missing or invalid reviewed box region: " + ident)
        annotations = row.get("annotations", [])
        source = data.get("sources", {}).get(row.get("source_id"))
        if not annotations or source is None:
            errors.append("Annotation/source evidence missing: " + ident)
            source = {}
        classes = {annotation.get("class_name") for annotation in annotations}
        if category not in {CLASS_CATEGORY.get(name) for name in classes}:
            errors.append("Category does not match the recorded annotations: " + ident)
        for annotation in annotations:
            name = annotation.get("class_name")
            cls = annotation.get("source_class_id")
            confidence = annotation.get("confidence")
            if name not in CLASS_CATEGORY:
                errors.append("Unknown annotation class: " + ident)
            if cls is not None and source.get("class_names", {}).get(str(cls)) != name:
                errors.append("Source class ID/name mismatch: " + ident)
            if confidence is not None:
                if not isinstance(confidence, (int, float)) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
                    errors.append("Invalid annotation confidence: " + ident)
                elif source.get("confidence_threshold") is not None and confidence < source["confidence_threshold"]:
                    errors.append("Prediction below its own source threshold: " + ident)
            if annotation.get("xyxyn") is not None and not valid_box(annotation["xyxyn"]):
                errors.append("Invalid recorded annotation coordinates: " + ident)
        if min(row.get("display_width", 0), row.get("display_height", 0)) <= 0:
            errors.append("Image dimensions missing: " + ident)
        for mode in ("after", "before"):
            filename = row.get(mode)
            if mode == "before" and filename is None:
                continue
            if not isinstance(filename, str):
                errors.append("Required gallery image missing: " + ident)
                continue
            relative = PurePosixPath(filename)
            if (relative.is_absolute() or ".." in relative.parts or len(relative.parts) != 2
                    or relative.parts[0] != category or relative.suffix.lower() != ".jpg"):
                errors.append("Unsafe or incorrectly organised image path: " + ident)
                continue
            path = assets / filename
            referenced.add(path.resolve())
            if not path.is_file() or path.is_symlink():
                errors.append("Gallery image missing or linked: " + filename)
            else:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if digest != row.get(mode + "_sha256"):
                    errors.append("Gallery image hash mismatch: " + filename)
                if mode == "after":
                    if digest in after_hashes:
                        errors.append("Duplicate annotated photo: " + ident)
                    after_hashes.add(digest)
        if row.get("before"):
            if row.get("before_sha256") == row.get("after_sha256"):
                errors.append("Unlabelled identical BEFORE/AFTER pair: " + ident)
            original = row.get("original_sha256")
            if not original or original in original_hashes:
                errors.append("Missing or duplicated original identity: " + ident)
            original_hashes.add(original)
            pairing = review.get("pairing", {})
            if pairing.get("mean_luma_difference", 999) >= 12:
                errors.append("Original/photo content match not verified: " + ident)
    actual = {p.resolve() for p in assets.rglob("*") if p.is_file()}
    for unused in actual - referenced:
        errors.append("Unselected asset in dedicated gallery folder: " + unused.name)
    serialized = json.dumps(data)
    if re.search(r"file:///|/Users/|[A-Za-z]:\\\\", serialized):
        errors.append("Private filesystem path in gallery data.")
    return errors
