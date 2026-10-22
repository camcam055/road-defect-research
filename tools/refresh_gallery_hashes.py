#!/usr/bin/env python3
"""Refresh file hashes after replacing gallery assets with real inference exports."""
from pathlib import Path
import hashlib,json
from layout import SITE
p=SITE/"data/gallery.json"
data=json.loads(p.read_text())
for row in data["images"]:
    for mode in ("before","after"):
        image=SITE/"assets/gallery"/row[mode]
        row[mode+"_sha256"]=hashlib.sha256(image.read_bytes()).hexdigest()
    if not row["predictions"] and row["before_sha256"]!=row["after_sha256"]:
        raise SystemExit("A no-detection example must use identical before and after files: "+row["id"])
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
print("Gallery file hashes updated. Rebuild sections and run check_site.py.")
