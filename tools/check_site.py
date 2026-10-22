#!/usr/bin/env python3
"""Buildless checks runnable on GitHub Actions with Python's standard library."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parent.parent
SITE=ROOT/"site"
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.links=[];self.ids=[];self.cards=[];self.images=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if "id" in d:self.ids.append(d["id"])
        if tag=="a" and "card" in d.get("class","").split():self.cards.append(d.get("href"))
        if tag=="img":
            self.images+=1
            if "alt" not in d:errors.append("Image missing alt text")
        for k in ("href","src"):
            if d.get(k):self.links.append(d[k])
errors=[];pages={};links=0
for p in SITE.rglob("*.html"):
    text=p.read_text()
    pg=Page();pg.feed(text);pages[p.resolve()]=pg
    if p.relative_to(SITE).as_posix()!="assets/map/index.html":
        if len(pg.ids)!=len(set(pg.ids)):errors.append(f"Duplicate IDs: {p.relative_to(SITE)}")
        if not re.search(r'<html[^>]+lang=',text):errors.append(f"No language: {p.name}")
    for pattern,name in [(r"file:///","local URL"),(r"/Users/[A-Za-z0-9]","private filesystem path"),(r"\bgh[pousr]_[A-Za-z0-9]{30,}","GitHub token"),(r"\bAKIA[A-Z0-9]{16}\b","AWS key"),(r"-----BEGIN .*PRIVATE KEY-----","private key")]:
        if re.search(pattern,text):errors.append(f"Privacy scan found {name}: {p.relative_to(SITE)}")
for p,pg in pages.items():
    refs=pg.links
    if p.relative_to(SITE).as_posix()=="assets/map/index.html":
        refs+=re.findall(r'(?:src|href)=["\']([^"\']+)["\']',p.read_text())
    for ref in refs:
        url=urlsplit(ref)
        if url.scheme or ref.startswith("//"):continue
        if ref.startswith("/"):errors.append(f"Root-relative path not repository-safe: {ref}");continue
        path=(p.parent/unquote(url.path)).resolve() if url.path else p
        if not path.is_relative_to(SITE.resolve()):errors.append(f"Link escapes public site: {ref}");continue
        if not path.exists():errors.append(f"Broken local link in {p.name}: {ref}")
        elif url.fragment and path in pages and unquote(url.fragment) not in pages[path].ids:
            errors.append(f"Broken anchor in {p.name}: {ref}")
        links+=1
for css in SITE.rglob("*.css"):
    for raw in re.findall(r"url\(([^)]+)\)",css.read_text()):
        ref=raw.strip().strip("\"'")
        url=urlsplit(ref)
        if url.scheme or ref.startswith(("//","#")):continue
        target=(css.parent/unquote(url.path)).resolve()
        if not target.is_relative_to(SITE.resolve()) or not target.is_file():errors.append(f"Broken CSS dependency in {css.name}: {ref}")
        links+=1
# JSON is the maintained source for the interactive pages.
import hashlib
for name,key in [("gallery","images"),("glossary","entries")]:
    data=json.loads((SITE/"data"/(name+".json")).read_text())
    if not data[key]:errors.append(f"Empty {name} data")
gallery=json.loads((SITE/"data/gallery.json").read_text())
if len(gallery["images"])<2:errors.append("Gallery examples missing")
for row in gallery["images"]:
    for view in ("before","after"):
        image=SITE/"assets/gallery"/row[view]
        if not image.is_file():errors.append(f"Missing {view} image: {row['id']}")
        elif hashlib.sha256(image.read_bytes()).hexdigest()!=row[view+"_sha256"]:errors.append(f"Gallery image hash mismatch: {row['id']} {view}")
    if not row["predictions"] and row["before_sha256"]!=row["after_sha256"]:errors.append("No-detection image must remain unchanged")
    for box in row["predictions"]:
        xy=box["xyxyn"]
        if not (len(xy)==4 and 0<=xy[0]<xy[2]<=1 and 0<=xy[1]<xy[3]<=1):errors.append("Invalid recorded box coordinates")
        if box["confidence"]<gallery["options"]["conf"]:errors.append("Prediction below the recorded threshold")
glossary=json.loads((SITE/"data/glossary.json").read_text())["entries"]
if len({r["term"].casefold() for r in glossary})!=len(glossary):errors.append("Duplicate glossary terms")
if "https://tile.openstreetmap.org/{z}/{x}/{y}.png" not in (SITE/"assets/map/index.html").read_text():errors.append("Working OSM basemap configuration missing")
if re.search(r'<script src="https?://', (SITE/"assets/map/index.html").read_text()):errors.append("Map runtime libraries are not bundled")
home=pages[(SITE/"index.html").resolve()]
expected=["video.html","map.html","content/problem.html","content/methodology.html","content/literature-review.html","content/results.html","content/conclusion.html","content/future-work.html","content/gallery.html","content/glossary.html"]
if home.cards!=expected:errors.append("Homepage card order/targets changed")
for p in SITE.rglob("*"):
    if p.is_symlink():errors.append(f"Symbolic link in deployment: {p.name}")
    if p.suffix.lower() in (".docx",".pptx",".pdf",".zip",".py",".md"):errors.append(f"Non-public source/review file in deployment: {p.name}")
    if p.name.startswith(".") and p.name!=".nojekyll":errors.append(f"Unexpected hidden deployment file: {p.name}")
video=(SITE/"video.html").read_text()
if "autoplay" in video or not all(x in video for x in ("controls","playsinline","video-placeholder")):errors.append("Video player requirements not met")
workflow=(ROOT/".github/workflows/pages.yml").read_text()
if "workflow_dispatch:" not in workflow or "publication_approved" not in workflow or "path: site" not in workflow:errors.append("Deployment approval gate missing")
if re.search(r"^\s+(push|pull_request):",workflow,re.M):errors.append("Automatic publication trigger found")
report={"status":"FAIL" if errors else "PASS","html_pages":len(pages),"homepage_cards":len(home.cards),"local_references_checked":links,"deployment_bytes":sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file()),"errors":errors}
print(json.dumps(report,indent=2));sys.exit(bool(errors))
