#!/usr/bin/env python3
"""Refresh gallery hashes; changing an asset invalidates its prior visual review."""
from pathlib import Path
import hashlib
import json
from layout import SITE

path = SITE / "data/gallery.json"
data = json.loads(path.read_text())
changed = []
for row in data["images"]:
    for mode in ("before", "after"):
        if not row.get(mode):
            continue
        image = SITE / "assets/gallery" / row[mode]
        digest = hashlib.sha256(image.read_bytes()).hexdigest()
        if row.get(mode + "_sha256") != digest:
            row["review"]["reviewed"] = False
            row["review"]["visible_box"] = False
            changed.append(row["id"])
        row[mode + "_sha256"] = digest
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
if changed:
    print("Changed assets need another visible-box and pairing review: " + ", ".join(sorted(set(changed))))
else:
    print("Gallery hashes already match the reviewed assets.")
