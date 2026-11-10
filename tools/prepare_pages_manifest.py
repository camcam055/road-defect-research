#!/usr/bin/env python3
"""Record the exact public files in a Pages artifact, without changing them."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("site"))
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        parser.error("--revision must be a full Git commit SHA")
    if not (args.site / "index.html").is_file():
        parser.error("the artifact must have index.html at its root")
    files = []
    for path in sorted(args.site.rglob("*")):
        if not path.is_file() or path == args.site / "deployment.json":
            continue
        if path.is_symlink():
            parser.error("symbolic links cannot be published")
        files.append({
            "path": path.relative_to(args.site).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    manifest = {"commit": args.revision, "files": files}
    (args.site / "deployment.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Prepared {len(files)} public files for revision {args.revision}")


if __name__ == "__main__":
    main()
