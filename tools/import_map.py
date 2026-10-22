#!/usr/bin/env python3
"""Copy the existing map, replacing local image URLs and scrubbing image metadata, with an optional basemap compatibility repair."""
import argparse,hashlib,json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
from extract_report import clean_image
def digest(b):return hashlib.sha256(b).hexdigest()
PLACEHOLDER='<svg xmlns="http://www.w3.org/2000/svg" width="640" height="400" viewBox="0 0 640 400"><rect width="640" height="400" fill="#edf6fe"/><text x="320" y="182" text-anchor="middle" font-family="Arial,sans-serif" font-size="25" fill="#092744">Photo withheld for privacy review</text><text x="320" y="222" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" fill="#536b80">The mapped defect information is unchanged.</text></svg>'
def main():
    p=argparse.ArgumentParser();p.add_argument("--source",type=Path,required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--audit",type=Path,required=True);p.add_argument("--withhold",action="append",default=[]);p.add_argument("--openstreetmap-basemap",action="store_true")
    a=p.parse_args()
    if a.audit.resolve().is_relative_to(a.output.resolve().parents[2]):raise SystemExit("Audit must be outside the repository")
    source=a.source.read_text();result=source;assets=[];inverse={}
    urls=sorted(set(re.findall(r'file://[^"\'<>]+',source)))
    a.output.mkdir(parents=True,exist_ok=True);(a.output/"photos").mkdir(exist_ok=True,parents=True)
    for n,url in enumerate(urls,1):
        f=Path(unquote(urlsplit(url).path))
        if not f.is_file():raise SystemExit(f"Missing source image #{n}; source map left untouched")
        withheld=f.name in a.withhold
        name=f"photos/withheld-{n:03d}.svg" if withheld else f"photos/photo-{n:03d}{f.suffix.lower()}"
        raw=f.read_bytes();data=PLACEHOLDER.encode() if withheld else clean_image(raw,f.suffix)
        (a.output/name).write_bytes(data);result=result.replace(url,name);inverse[name]=url
        assets.append({"asset":name,"source_url_sha256":digest(url.encode()),"source_sha256":digest(raw),"public_sha256":digest(data),"status":"withheld for review" if withheld else "copied; pixel data unchanged; metadata removed"})
    lazy_tag='<img loading="lazy" decoding="async" src='
    image_count=result.count("<img src=")
    result=result.replace("<img src=",lazy_tag)
    web_replacements={}
    if a.openstreetmap_basemap:
        start=result.index("L.tileLayer(")
        end=result.index(");",start)+2
        original=result[start:end]
        updated=original.replace("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png","https://tile.openstreetmap.org/{z}/{x}/{y}.png")
        if updated==original:raise SystemExit("Review the supplied basemap before applying this repair")
        updated=updated.replace('"maxNativeZoom": 20','"maxNativeZoom": 19')
        updated=re.sub(r'"attribution": .*?,\n',lambda _: '"attribution": '+json.dumps('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')+',\n',updated,count=1)
        result=result[:start]+updated+result[end:]
        web_replacements[updated]=original
    restored=result.replace(lazy_tag,"<img src=")
    for updated,original in web_replacements.items():restored=restored.replace(updated,original,1)
    for name,url in inverse.items():restored=restored.replace(name,url)
    if restored!=source:raise SystemExit("Unexpected map content change")
    if "file://" in result or "/Users/" in result:raise SystemExit("Unresolved local path")
    # Presentation adapter is separate; the original map scripts and geographic data remain untouched.
    result=result.replace("</head>",'<title>Road defect research map</title><link rel="stylesheet" href="map-adapter.css"></head>',1)
    result=result.replace("</html>",'<script src="map-adapter.js" defer></script></html>',1)
    (a.output/"index.html").write_text(result)
    a.audit.mkdir(parents=True,exist_ok=True)
    report={"source_sha256":digest(source.encode()),"public_sha256":digest(result.encode()),"original_map_roundtrip":"PASS","explanation":"Before adding the display adapter, reversing photo URL, lazy-image markup and documented basemap replacements reproduces the entire original map exactly. Geographic data, defect values, overlay definitions and colors are unchanged.","lazy_popup_images":image_count,"basemap_repair":"OpenStreetMap HTTPS tile URL, attribution and native zoom limit; original CARTO tiles returned API-key-required images." if a.openstreetmap_basemap else None,"assets":assets}
    (a.audit/"map-audit.json").write_text(json.dumps(report,indent=2))
    print(json.dumps({"status":"PASS","linked_photos":len(urls),"withheld_photos":sum(x["status"].startswith("withheld") for x in assets),"map_data_roundtrip":"PASS"}))
if __name__=="__main__":main()
