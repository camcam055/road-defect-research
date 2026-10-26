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
from gallery_checks import check_gallery
gallery=json.loads((SITE/"data/gallery.json").read_text())
errors.extend(check_gallery(gallery,SITE/"assets/gallery"))
glossary=json.loads((SITE/"data/glossary.json").read_text())["entries"]
if len({r["term"].casefold() for r in glossary})!=len(glossary):errors.append("Duplicate glossary terms")
if "https://tile.openstreetmap.org/{z}/{x}/{y}.png" not in (SITE/"assets/map/index.html").read_text():errors.append("Working OSM basemap configuration missing")
if re.search(r'<script src="https?://', (SITE/"assets/map/index.html").read_text()):errors.append("Map runtime libraries are not bundled")
# Validate the downloadable observation export alongside its map photos.
import csv
map_source=json.loads((SITE/"data/map-source.json").read_text())
with (SITE/"assets/map/observations.csv").open(newline="") as stream:
    observations=list(csv.DictReader(stream))
if len(observations)!=map_source["all_observations_csv_rows"]:errors.append("Map observation count does not match provenance")
located=sum(bool(row["lat"] and row["lon"]) for row in observations)
if located!=map_source["located_observations"]:errors.append("Located map observations do not match provenance")
for row in observations:
    ref=row.get("image_url","")
    if not ref:continue
    target=(SITE/"assets/map"/ref).resolve()
    if urlsplit(ref).scheme or not target.is_relative_to(SITE.resolve()) or not target.is_file():errors.append("Observation CSV has an unavailable photo")
    links+=1
for public in SITE.rglob("*"):
    if public.is_file() and public.suffix in (".csv",".json"):
        content=public.read_text()
        if re.search(r"file:///|/Users/[A-Za-z0-9]|-----BEGIN .*PRIVATE KEY-----",content):errors.append(f"Private data path or key in {public.relative_to(SITE)}")
    if public.is_file() and public.stat().st_size>=100*1024*1024:errors.append(f"File exceeds GitHub size limit: {public.relative_to(SITE)}")
map_html=(SITE/"assets/map/index.html").read_text()
defect_controls=re.findall(r'"(Road defects[^"]*)"\s*:\s*feature_group_',map_html)
if defect_controls!=["Road defects"]:
    errors.append("Run-specific defect labels reappeared in map controls")
map_wrapper=(SITE/"map.html").read_text()
if any(term in map_wrapper for term in ('class="map-toolbar"', 'class="map-status"', 'class="site-header"')):errors.append("Map wrapper contains removed page text")
if "inspection-card" in (SITE/"assets/map/index.html").read_text():errors.append("Removed inspection summary reappeared")
if 'class="map-back"' not in map_wrapper:errors.append("Full-page map Back link missing")
# Preserve the requested map interpretation and front-matter exclusion.
if re.search(r"executive\s+summary", " ".join(p.read_text() for p in SITE.rglob("*.html")), re.I):
    errors.append("Excluded Executive Summary text found")
if map_wrapper.count('class="map-relationships"')!=1 or map_wrapper.index('class="map-relationships"')<map_wrapper.index("</iframe>"):
    errors.append("Map interpretation must appear once directly below the map")
for required in ("Exploring Potential Relationships","High Traffic + Many Defects:","Less Favourable Soil Conditions + Many Defects:","Low Traffic + Many Defects:","These relationships are possible explanations rather than confirmed causes."):
    if required not in map_wrapper:errors.append("Requested map interpretation text missing")
home=pages[(SITE/"index.html").resolve()]
expected=["video.html","map.html","content/problem.html","content/literature-review.html","content/methodology.html","content/results.html","content/conclusion.html","content/future-work.html","content/gallery.html","content/glossary.html"]
if [urlsplit(card).path for card in home.cards]!=expected:errors.append("Homepage card order/targets changed")
# Owner-approved research order and administrative-content exclusions.
for slug,number in (("literature-review","02"),("methodology","03")):
    if f'<p class="eyebrow">SECTION {number}</p>' not in (SITE/"content"/(slug+".html")).read_text():
        errors.append(f"Incorrect section number: {slug}")
for slug,bid,number in (("conclusion","b1501","5.0"),("future-work","b1435","6.0"),("results","b1346","4.5")):
    text=(SITE/"content"/(slug+".html")).read_text()
    if f'data-source-id="{bid}">{number} ' not in text or f'href="#{bid}">{number} ' not in text:
        errors.append(f"Heading and contents numbering disagree: {slug}")
for public in SITE.rglob("*"):
    if public.is_file() and public.suffix in (".html",".json",".js",".css",".csv"):
        text=public.read_text()
        if re.search(r"project\s+management|progress to date and timeline|risks, mitigation and challenges|cost considerations",text,re.I):
            errors.append(f"Excluded administrative content in {public.relative_to(SITE)}")
        if any(1407<=int(b)<1435 or 1454<=int(b)<1501 for b in re.findall(r"\bb(\d{4})\b",text)):
            errors.append(f"Removed source block or anchor in {public.relative_to(SITE)}")
for p in SITE.rglob("*"):
    if p.is_symlink():errors.append(f"Symbolic link in deployment: {p.name}")
    if p.suffix.lower() in (".docx",".pptx",".pdf",".zip",".py",".md"):errors.append(f"Non-public source/review file in deployment: {p.name}")
    if p.name.startswith(".") and p.name!=".nojekyll":errors.append(f"Unexpected hidden deployment file: {p.name}")
from video_checks import check_video_site
errors.extend(check_video_site(SITE))
workflow=(ROOT/".github/workflows/pages.yml").read_text()
if "workflow_dispatch:" not in workflow or "publication_approved" not in workflow or "path: site" not in workflow:errors.append("Deployment approval gate missing")
if re.search(r"^\s+(push|pull_request):",workflow,re.M):errors.append("Automatic publication trigger found")
report={"status":"FAIL" if errors else "PASS","html_pages":len(pages),"homepage_cards":len(home.cards),"local_references_checked":links,"deployment_bytes":sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file()),"errors":errors}
print(json.dumps(report,indent=2));sys.exit(bool(errors))
