"""Shared page layout, separate from report content."""
from html import escape
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SECTIONS = [("problem","THE PROBLEM"),("literature-review","LITERATURE REVIEW"),("methodology","METHODOLOGY"),("results","RESULTS"),("conclusion","CONCLUSION"),("future-work","FUTURE WORK"),("gallery","PHOTO GALLERY"),("glossary","TECHNICAL GLOSSARY")]
ARROW = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" stroke-width="2.1"/></svg>'
BACK = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m10 5-7 7 7 7M3 12h18" stroke="currentColor" stroke-width="1.8"/></svg>'
PLAY = '<svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="48" fill="currentColor"/><path d="M39 30q-4-2-4 3v34q0 5 4 3l31-18q4-2 0-4Z" fill="white"/></svg>'
PIN = '<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M50 3C27 3 13 21 13 41c0 23 37 56 37 56s37-33 37-56C87 21 73 3 50 3Z" fill="currentColor"/><circle cx="50" cy="38" r="12" fill="white"/></svg>'
def document(title,body,prefix="",cls=""):
    cache_version="?v=20261026-final" if cls=="map-body" else ""
    return f'''<!doctype html>
<html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Campbell Searle's civil engineering research on AI road surface defect detection."><meta name="theme-color" content="#092744"><title>{escape(title)} · Road defect research</title><link rel="stylesheet" href="{prefix}css/styles.css{cache_version}"><script src="{prefix}js/config.js" defer></script><script src="{prefix}js/main.js{cache_version}" defer></script></head><body class="{cls}"><a class="skip-link" href="#main">Skip to content</a>{body}</body></html>'''
def header(prefix=""):
    return f'<header class="site-header"><div class="header-inner"><a class="home-link" href="{prefix}index.html">{BACK}All sections</a><span class="header-context">Campbell Searle<br>MG7101 · Engineering Development Project</span></div></header>'
def section_page(slug,title,article,headings,notice="",source_note=None,wide=False):
    idx=next((i for i,(s,t) in enumerate(SECTIONS) if s==slug),None)
    num=f"SECTION {idx+1:02d}" if idx is not None else "SOURCE MATERIAL"
    toc='<details class="toc"><summary>On this page</summary><ol>'+''.join(f'<li><a href="#{escape(a)}">{escape(t)}</a></li>' for a,t in headings)+'</ol></details>'
    foot='<a href="../index.html">← All sections</a>'
    if idx is not None:
        if idx: foot=f'<a href="{SECTIONS[idx-1][0]}.html">← {SECTIONS[idx-1][1].title()}</a>'
        foot+=f'<a href="{SECTIONS[idx+1][0]}.html">{SECTIONS[idx+1][1].title()} →</a>' if idx<len(SECTIONS)-1 else '<a href="../index.html">All sections →</a>'
    if not headings: toc=""
    note=source_note if source_note is not None else 'Research report · Updated 26 October 2026. Section numbering follows the website navigation. <a href="references.html">References</a>'
    source_markup=f'<p class="source-note">{note}</p>' if note else ""
    reading_class="reading-layout wide-layout" if wide else "reading-layout"
    body=header("../")+f'<main id="main" class="page-shell"><div class="page-heading"><p class="eyebrow">{num}</p><h1>{escape(title.title())}</h1>{source_markup}</div>{notice}<div class="{reading_class}">{toc}<article class="report-content">{article}</article></div><nav class="page-footer" aria-label="Section navigation">{foot}</nav><div class="bottom-meta">Campbell Searle · Ara Institute of Canterbury · 2026</div></main>'
    (SITE/"content").mkdir(parents=True,exist_ok=True)
    (SITE/"content"/f"{slug}.html").write_text(document(title,body,"../"),encoding="utf-8")
def build_home():
    cards=""
    for slug,title,icon in [("video","PROJECT VIDEO",PLAY),("map","INTERACTIVE MAP",PIN)]:
        map_version="?v=20261026-final" if slug=="map" else ""
        cards+=f'<a class="card featured" href="{slug}.html{map_version}"><span class="featured-icon">{icon}</span><h2>{title}</h2><span class="card-arrow">{ARROW}</span></a>'
    for i,(slug,title) in enumerate(SECTIONS,1):
        cards+=f'<a class="card research" href="content/{slug}.html"><span class="card-number" aria-hidden="true">{i:02}</span><h2>{title}</h2><span class="card-arrow">{ARROW}</span></a>'
    body=f'<main class="home" id="main"><h1 class="sr-only">Road surface defect detection research</h1><nav class="cards" aria-label="Explore the research">{cards}</nav><footer class="home-footer">Campbell Searle · MG7101 · 2026</footer></main>'
    (SITE/"index.html").write_text(document("Explore the research",body),encoding="utf-8")
def build_shell():
    build_home()
    from video_page import render_video
    (SITE/"video.html").write_text(render_video(document,header),encoding="utf-8")
    body='''<a class="map-back" href="index.html" aria-label="Back to all research sections">← Back</a><main id="main"><div class="map-frame-wrap"><iframe class="map-frame" id="defect-map" src="assets/map/index.html?v=20261026-labels" title="Interactive road defect detection map" allowfullscreen></iframe></div><section class="map-relationships" aria-labelledby="map-relationships-title"><div class="map-relationships-inner"><h1 id="map-relationships-title">Exploring Potential Relationships</h1><p class="map-relationships-intro">The interactive map allows users to explore potential relationships between traffic volumes, soil conditions and pavement defects.</p><ul class="map-relationship-grid"><li><h2>High Traffic + Many Defects:</h2><p>May indicate pavement deterioration associated with repeated vehicle loading.</p></li><li><h2>Less Favourable Soil Conditions + Many Defects:</h2><p>May suggest that underlying ground conditions warrant further investigation.</p></li><li><h2>Low Traffic + Many Defects:</h2><p>May indicate other contributing factors, such as pavement ageing, drainage problems or construction quality.</p></li></ul><p class="map-relationships-important"><strong>Important:</strong> These relationships are possible explanations rather than confirmed causes. Further engineering investigation would be required to establish whether these factors contribute to pavement deterioration.</p></div></section></main>'''
    (SITE/"map.html").write_text(document("Interactive map",body,cls="map-body"),encoding="utf-8")
    (SITE/".nojekyll").touch()
    (SITE/"assets/video").mkdir(parents=True,exist_ok=True)
if __name__=="__main__": build_shell()
