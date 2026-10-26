#!/usr/bin/env python3
"""Build the reviewed, category-grouped gallery without changing report pages."""
from collections import Counter
from html import escape
import json
from layout import SITE, section_page

NAMES = {
    "long_crack": "Longitudinal crack",
    "lateral_crack": "Transverse crack",
    "alligator_crack": "Alligator cracking",
    "pothole": "Pothole",
    "other_corruption": "Other surface defect",
}

def card(row, sources):
    ident = escape(row["id"], quote=True)
    title = escape(row["title"])
    after = "../assets/gallery/" + escape(row["after"], quote=True)
    before = "../assets/gallery/" + escape(row["before"], quote=True) if row.get("before") else None
    summaries = []
    for annotation in row["annotations"]:
        label = NAMES[annotation["class_name"]]
        confidence = annotation.get("confidence")
        text = f"{label}: {confidence * 100:.1f}% confidence" if confidence is not None else f"{label}: saved annotation"
        if text not in summaries:
            summaries.append(text)
    summary = "; ".join(summaries)
    alt = escape(row["title"] + " — " + summary + " — visible road-defect bounding boxes", quote=True)
    width, height = row["display_width"], row["display_height"]
    switch = '<p class="gallery-unpaired">Labelled photo · Original unavailable</p>'
    original = ""
    if before:
        switch = f'''<div class="gallery-switch" role="group" aria-label="Choose view for {escape(row["title"], quote=True)}">
<button type="button" data-view="before" aria-pressed="false" aria-controls="{ident}-images">BEFORE</button>
<button type="button" data-view="after" aria-pressed="true" aria-controls="{ident}-images">AFTER</button></div>'''
        original = f'<img data-image="before" src="{before}" alt="{escape(row["title"] + " — matching original photograph", quote=True)}" width="{width}" height="{height}" loading="lazy" decoding="async" hidden>'
    return f'''<section class="gallery-card" data-gallery data-category="{escape(row["category"], quote=True)}" id="{ident}" aria-labelledby="{ident}-title">
<h3 id="{ident}-title">{title}</h3>{switch}
<figure><div class="gallery-images" id="{ident}-images">{original}<img data-image="after" src="{after}" alt="{alt}" width="{width}" height="{height}" loading="lazy" decoding="async"></div>
<figcaption><p class="gallery-state" aria-live="polite">After · Saved labelled photograph</p>
<p>{escape(summary)}</p>
<a class="gallery-full" href="{after}" target="_blank" rel="noopener">Open current image at full size ↗</a></figcaption></figure></section>'''

def build_gallery():
    data = json.loads((SITE / "data/gallery.json").read_text())
    if data.get("schema_version") != 2:
        raise ValueError("The gallery requires the reviewed version 2 manifest.")
    for row in data["images"]:
        if not row.get("annotations") or not row.get("review", {}).get("visible_box") or not row["review"].get("reviewed"):
            raise ValueError("Gallery image requires a completed visible-box review: " + row["id"])
    counts = Counter(row["category"] for row in data["images"])
    total = len(data["images"])
    filters = f'<button type="button" data-gallery-filter="all" aria-pressed="true" aria-controls="gallery-categories">All photos ({total})</button>'
    sections = []
    for category in data["categories"]:
        ident = escape(category["id"], quote=True)
        title = escape(category["title"])
        count = counts[category["id"]]
        if not count:
            continue
        filters += f'<button type="button" data-gallery-filter="{ident}" aria-pressed="false" aria-controls="gallery-categories">{title} ({count})</button>'
        cards = "".join(card(row, data["sources"]) for row in data["images"] if row["category"] == category["id"])
        sections.append(f'<section class="gallery-category" data-gallery-category="{ident}" aria-labelledby="category-{ident}"><h2 id="category-{ident}">{title} <span class="gallery-category-count">({count})</span></h2><div class="gallery-grid">{cards}</div></section>')
    intro = f'''<p class="interactive-intro">Browse labelled road-defect photographs by category. Every example opens with its saved bounding boxes visible. Select <strong>BEFORE</strong> to compare a confirmed matching original.</p>
<div class="gallery-filters" role="group" aria-label="Filter photographs by defect category">{filters}</div>
<p id="gallery-count" class="gallery-count" role="status" aria-live="polite">{total} photos</p>
<noscript><p class="notice">All labelled photographs are shown below. Enable JavaScript to filter categories or compare original photographs.</p></noscript>'''
    section_page("gallery", "PHOTO GALLERY", intro + '<div id="gallery-categories">' + "".join(sections) + "</div>", [],
                 source_note="", wide=True)
    return total
