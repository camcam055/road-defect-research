#!/usr/bin/env python3
"""Import the supplied master map without changing its observations or layers."""
import argparse, csv, hashlib, io, json, re, shutil
from datetime import datetime
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo
from extract_report import clean_image
from layout import SITE

def digest(data):
    return hashlib.sha256(data).hexdigest()

def public_reference(reference, prefix):
    return reference[len(prefix):] if reference.startswith(prefix) else reference


def combine_defect_controls(source):
    """Create one defect switch before the map control is rendered."""
    entries=list(re.finditer(r'(?m)^(?P<indent>[ \t]*)"Road defects[^"\n]*"\s*:\s*(?P<layer>feature_group_[A-Za-z0-9_]+),[ \t]*$',source))
    if len(entries)<2:
        return source
    map_name=re.search(r'var (map_[A-Za-z0-9_]+)\s*=\s*L.map\(',source).group(1)
    control=re.search(r'var layer_control_[A-Za-z0-9_]+_layers\s*=\s*\{',source)
    if control is None or any(entry.start()<control.start() for entry in entries):
        raise ValueError("Unexpected road-defect control layout")
    combined="feature_group_research_road_defects"
    for index,entry in reversed(list(enumerate(entries))):
        replacement=entry.group("indent")+'"Road defects" : '+combined+',' if index==0 else ""
        source=source[:entry.start()]+replacement+source[entry.end():]
    declaration='var '+combined+' = L.featureGroup(['+','.join(entry.group("layer") for entry in entries)+']).addTo('+map_name+');\n            '
    return source[:control.start()]+declaration+source[control.start():]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,required=True)
    parser.add_argument("--audit",type=Path,required=True)
    args=parser.parse_args()
    if args.audit.resolve().is_relative_to(SITE.parent.resolve()):
        raise SystemExit("Source audit must remain outside the repository")
    source=args.source.read_text()
    if re.search(r"file://|/Users/",source):
        raise SystemExit("Review private paths before importing")
    match=re.search(r'<meta name="road-defect-assets" content="([^"]+)">',source)
    asset_base=match.group(1) if match else args.source.stem+"_assets"
    asset_root=args.source.parent/asset_base
    if not asset_root.is_dir():
        raise SystemExit("The master map and its supporting assets must stay together")
    prefix=asset_base+"/"
    observations=(asset_root/"observations.csv").read_text()
    rows=list(csv.DictReader(io.StringIO(observations)))
    references=set(re.findall(r'(?:src|href)=["\']([^"\']+)["\']',source))
    references.update(row["image_url"] for row in rows if row["image_url"])
    local={ref for ref in references if not urlsplit(ref).scheme and not ref.startswith(("//","#","data:"))}
    photos=sorted(ref for ref in local if PurePosixPath(ref).suffix.lower() in (".jpg",".jpeg",".png") and "/vendor/" not in ref)
    if not photos:
        raise SystemExit("No master-map photographs found")
    for ref in local:
        relative=PurePosixPath(ref)
        path=(args.source.parent/ref).resolve()
        if relative.is_absolute() or ".." in relative.parts or not path.is_relative_to(args.source.parent.resolve()) or not path.is_file():
            raise SystemExit("Missing or unsafe master-map asset: "+ref)
    manifest=json.loads((asset_root/"image_manifest.json").read_text())
    withheld={"run12/frame_0038.jpg","run12/frame_0060.jpg","run12/frame_0067.jpg"}
    for row in manifest:
        if row["source"] in withheld and (row["file"] in photos or prefix+row["file"] in photos):
            raise SystemExit("Previously withheld photographs need an explicit privacy review")
    coverage_file=asset_root/"run_coverage.json"
    coverage=json.loads(coverage_file.read_text()) if coverage_file.exists() else None
    if coverage and source.count("L.marker(")!=coverage["mapped_markers"]:
        raise SystemExit("Source marker count differs from coverage")
    output=SITE/"assets/map";output.mkdir(parents=True,exist_ok=True)
    args.audit.mkdir(parents=True,exist_ok=True)
    records=[]
    for n,ref in enumerate(photos,1):
        raw=(args.source.parent/ref).read_bytes()
        cleaned=clean_image(raw,Path(ref).suffix)
        relative=public_reference(ref,prefix)
        dest=output/relative;dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(cleaned)
        records.append({"file":relative,"source_sha256":digest(raw),"public_sha256":digest(cleaned)})
        if n%100==0:print(f"Verified {n}/{len(photos)} map photographs",flush=True)
    for path in (asset_root/"vendor").rglob("*"):
        if path.is_file():
            dest=output/"vendor"/path.relative_to(asset_root/"vendor")
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,dest)
    public_observations=observations.replace(prefix,"")
    (output/"observations.csv").write_text(public_observations)
    canonical=combine_defect_controls(source.replace(prefix,"").replace('content="'+asset_base+'"','content="."'))
    head='<title>Road defect research map</title><link rel="stylesheet" href="map-adapter.css?v=20261026-final">'
    control_name=re.search(r'(?:var|let|const) (layer_control_[a-zA-Z0-9_]+) = L.control.layers',source).group(1)
    tail='<script>window.RESEARCH_MAP_CONTEXT={control:'+control_name+',layers:'+control_name+'_layers};</script><script src="map-adapter.js?v=20261026-labels" defer></script>'

    public=canonical.replace("</head>",head+"</head>",1).replace("</html>",tail+"</html>",1)
    if public.replace(head,"",1).replace(tail,"",1)!=canonical:
        raise SystemExit("Unexpected map change")
    (output/"index.html").write_text(public)
    located=sum(bool(row["lat"] and row["lon"]) for row in rows)
    summary={
        "source":"Latest supplied master road-defect map",
        "source_saved":datetime.fromtimestamp(args.source.stat().st_mtime,ZoneInfo("Pacific/Auckland")).strftime("%d %B %Y").lstrip("0"),
        "source_sha256":digest(source.encode()),"public_sha256":digest(public.encode()),
        "verification":"Entire map matches the source after relative asset paths, a page title, one combined Road defects control and the separate website navigation adapter. Marker coordinates, grouped observations, PDI visualisations, geographic features, popups and qualifications are unchanged. Referenced photographs retain identical pixels with private metadata removed.",
        "website_layer_adjustments":["All road-defect runs share one Road defects toggle, as requested by the owner. Original clusters, markers and popup run details are retained."] ,
        "marker_count":source.count("L.marker("),
        "tentative_defect_locations":coverage["mapped_markers"] if coverage else source.count("L.marker("),
        "located_observations":located,"observations_without_gps":len(rows)-located,
        "all_observations_csv_rows":len(rows),"map_photographs":len(photos),
        "qualifications":["Grouping is conservative and provisional; GPS marks the camera position.","Grey density sections are not assessable.","Mapped detections and visual observations do not establish measured accuracy.","All saved runs in the supplied master export are retained; only records with usable GPS can be mapped.","Earlier-run markers contain all detections in each source photograph; separate runs are not deduplicated against one another."]
    }
    if coverage:
        for key in ("display_scope","runs","mapped_observations","observations_excluded_from_map","display_exclusions"):
            summary[key]=coverage[key]
    (SITE/"data/map-source.json").write_text(json.dumps(summary,indent=2)+"\n")
    (args.audit/"map-audit.json").write_text(json.dumps({**summary,"assets":records},indent=2)+"\n")
    print(json.dumps({"status":"PASS",**{k:summary[k] for k in ("marker_count","located_observations","observations_without_gps","map_photographs")}},indent=2))

if __name__=="__main__":main()
