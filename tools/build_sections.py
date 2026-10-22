#!/usr/bin/env python3
"""Regenerate sections 07 and 08 from their public JSON files; standard library only."""
from pathlib import Path
from html import escape
import json
from layout import SITE,section_page

def build():
    gallery=json.loads((SITE/'data/gallery.json').read_text())
    cards=[]
    names={'long_crack':'Longitudinal crack','lateral_crack':'Transverse crack','pothole':'Pothole','alligator_crack':'Alligator cracking','other_corruption':'Other surface defect'}
    for row in gallery['images']:
        ident=escape(row['id'],quote=True)
        before='../assets/gallery/'+row['before'];after='../assets/gallery/'+row['after']
        count=len(row['predictions'])
        summary='; '.join(f"{names.get(p['class_name'],p['class_name'])}: {p['confidence']*100:.1f}% confidence" for p in row['predictions']) if count else 'No detection at the 0.40 confidence threshold.'
        note='The displayed boxes are saved model predictions. Visible defects can be missed or misclassified.' if count else 'A visible crack is present, but this model returned no detection. No box has been added.'
        alt=escape(row['title']+' — original road photograph',quote=True)
        afteralt=escape(row['title']+' — '+summary,quote=True)
        cards.append(f'''<section class="gallery-card" data-gallery id="{ident}" aria-labelledby="{ident}-title">
<h2 id="{ident}-title">{escape(row['title'])}</h2>
<div class="gallery-switch" role="group" aria-label="Choose view for {escape(row['title'],quote=True)}">
<button type="button" data-view="before" aria-pressed="true" aria-controls="{ident}-images">BEFORE</button>
<button type="button" data-view="after" aria-pressed="false" aria-controls="{ident}-images">AFTER</button></div>
<figure><div class="gallery-images" id="{ident}-images"><img data-image="before" src="{before}" alt="{alt}" width="{row['display_width']}" height="{row['display_height']}" loading="lazy" decoding="async"><img data-image="after" src="{after}" alt="{afteralt}" width="{row['display_width']}" height="{row['display_height']}" loading="lazy" decoding="async" hidden></div>
<figcaption><p class="gallery-state" aria-live="polite">Before · Original photograph</p><p>{escape(summary)}</p><p>{escape(note)}</p><a class="gallery-full" href="{before}" target="_blank" rel="noopener">Open current image at full size ↗</a></figcaption></figure></section>''')
    intro='<p class="interactive-intro">Select <strong>BEFORE</strong> for the original photograph or <strong>AFTER</strong> for the same image with the recorded YOLO predictions.</p><aside class="notice">These are genuine saved predictions from the project’s YOLO checkpoint, run on 22 October 2026 at a confidence threshold of 0.40. They illustrate model behaviour, including missed defects. Confidence scores are not accuracy measurements. <a href="../data/gallery.json">View prediction data and provenance</a>.</aside><noscript><p class="notice">Enable JavaScript for the BEFORE/AFTER buttons. The <a href="../data/gallery.json">prediction data</a> lists the original and annotated image filenames.</p></noscript>'
    article=intro+'<div class="gallery-grid">'+''.join(cards)+'</div>'
    section_page('gallery','PHOTO GALLERY',article,[],source_note='Original project photographs and recorded model predictions. <a href="methodology.html#b0866">Detection workflow</a> · <a href="results.html#b1124">Model limitations</a>',wide=True)
    glossary=json.loads((SITE/'data/glossary.json').read_text())
    entries=[]
    for n,row in enumerate(glossary['entries'],1):
        text=' '.join([row['term'],row['definition'],row.get('aliases','')])
        entries.append(f'<div class="glossary-entry" data-search="{escape(text,quote=True)}"><dt id="term-{n:02d}">{escape(row["term"])}</dt><dd><p>{escape(row["definition"])}</p><a href="{escape(row["source"],quote=True)}">{escape(row["source_label"])} ↗</a></dd></div>')
    total=len(entries)
    article=f'''<p class="interactive-intro">Plain-language definitions drawn from the existing research. Each entry links to its source passage. Search by term, abbreviation or a word in the definition.</p><div class="glossary-search" role="search"><label for="glossary-search">Search the technical glossary</label><div class="search-row"><input id="glossary-search" type="search" placeholder="Try PDI, YOLO, cracking…" autocomplete="off" aria-controls="glossary-list"><button id="glossary-clear" type="button">Clear</button></div><p id="glossary-count" role="status" aria-live="polite">{total} terms</p></div><noscript><p class="notice">All glossary entries are shown below. Enable JavaScript to search.</p></noscript><p id="glossary-empty" class="notice" hidden>No matching terms. Try a shorter word, an abbreviation, or Clear.</p><dl id="glossary-list" class="glossary-list">{''.join(entries)}</dl>'''
    section_page('glossary','TECHNICAL GLOSSARY',article,[],source_note='Based on the latest supplied research report. Definitions are concise explanations; follow the source links for the report wording.',wide=True)
    print(f'Sections built: {len(cards)} genuine gallery examples; {total} searchable glossary terms.')
if __name__=='__main__':build()
