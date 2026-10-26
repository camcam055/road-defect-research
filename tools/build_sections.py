#!/usr/bin/env python3
"""Regenerate sections 07 and 08 from their public JSON files; standard library only."""
from pathlib import Path
from html import escape
import json
from layout import SITE,section_page

def build():
    from gallery_page import build_gallery
    card_count=build_gallery()
    glossary=json.loads((SITE/'data/glossary.json').read_text())
    entries=[]
    for n,row in enumerate(glossary['entries'],1):
        text=' '.join([row['term'],row['definition'],row.get('aliases','')])
        entries.append(f'<div class="glossary-entry" data-search="{escape(text,quote=True)}"><dt id="term-{n:02d}">{escape(row["term"])}</dt><dd><p>{escape(row["definition"])}</p><a href="{escape(row["source"],quote=True)}">{escape(row["source_label"])} ↗</a></dd></div>')
    total=len(entries)
    article=f'''<p class="interactive-intro">Plain-language definitions drawn from the existing research. Each entry links to its source passage. Search by term, abbreviation or a word in the definition.</p><div class="glossary-search" role="search"><label for="glossary-search">Search the technical glossary</label><div class="search-row"><input id="glossary-search" type="search" placeholder="Try PDI, YOLO, cracking…" autocomplete="off" aria-controls="glossary-list"><button id="glossary-clear" type="button">Clear</button></div><p id="glossary-count" role="status" aria-live="polite">{total} terms</p></div><noscript><p class="notice">All glossary entries are shown below. Enable JavaScript to search.</p></noscript><p id="glossary-empty" class="notice" hidden>No matching terms. Try a shorter word, an abbreviation, or Clear.</p><dl id="glossary-list" class="glossary-list">{''.join(entries)}</dl>'''
    section_page('glossary','TECHNICAL GLOSSARY',article,[],source_note="",wide=True)
    print(f'Sections built: {card_count} reviewed labelled gallery examples; {total} searchable glossary terms.')
if __name__=='__main__':build()
