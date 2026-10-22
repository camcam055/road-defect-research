#!/usr/bin/env python3
"""Bundle dependencies of a reviewed Folium HTML export for static hosting."""
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
import argparse,hashlib,json,re,urllib.request
from layout import SITE

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--map',type=Path,default=SITE/'assets/map/index.html')
    args=ap.parse_args();page=args.map.resolve();out=page.parent/'vendor';out.mkdir(exist_ok=True)
    manifest=out/'sources.json';records={r['file']:r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    def get(url,force=False):
        if urlsplit(url).scheme!='https':raise ValueError('Only HTTPS dependency downloads are supported')
        name=unquote(urlsplit(url).path.rsplit('/',1)[-1])
        if not name or name in ('.','..') or '/' in name:raise ValueError('Unsafe dependency filename')
        dest=out/name
        old=records.get(name)
        # Never reuse a file from a different URL/version merely because its basename matches.
        if force or not dest.exists() or not old or old['source']!=url:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RoadDefectResearch-local-build/1.0'}),timeout=30) as r:raw=r.read()
            dest.write_bytes(raw)
            records[name]={'file':name,'source':url,'sha256':hashlib.sha256(raw).hexdigest()}
        return dest
    text=page.read_text()
    urls=re.findall(r'(?:<script src="|<link rel="stylesheet" href=")(https://[^\"]+)',text)
    for url in urls:
        dest=get(url,force=urlsplit(url).path.endswith('.css'))
        if dest.suffix=='.css':
            css=dest.read_text()
            for match in list(re.finditer(r'url\(([\"\']?)([^)\"\']+)\1\)',css)):
                ref=match.group(2)
                if ref.startswith(('data:','#')):continue
                asseturl=urljoin(url,ref).split('#')[0].split('?')[0]
                asset=get(asseturl);css=css.replace(ref,asset.name)
            css=re.sub(r'/\*# sourceMappingURL=.*?\*/','',css);dest.write_text(css)
        text=text.replace(url,'vendor/'+dest.name)
    text=text.replace('<html>','<html lang="en-NZ">',1)
    text=text.replace('initial-scale=1.0, maximum-scale=1.0, user-scalable=no','initial-scale=1.0')
    page.write_text(text)
    for row in records.values():
        local=out/row['file']
        if local.exists():row['local_sha256']=hashlib.sha256(local.read_bytes()).hexdigest()
    manifest.write_text(json.dumps(list(records.values()),indent=2)+'\n')
    print('Map dependencies bundled; '+str(len(urls))+' external references replaced. Check vendor licenses when introducing a new library.')
if __name__=='__main__':main()
