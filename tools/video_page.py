"""Render the project video page from the three reviewed final video assets."""
from html import escape
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

def duration_label(seconds):
    rounded = int(float(seconds) + 0.5)
    return f"{rounded // 60}:{rounded % 60:02d}"

def render_video(document, header):
    videos = json.loads((SITE / "data/videos.json").read_text())["videos"]
    first = videos[0]
    captions = ["Collect road imagery", "Train the model", "See the detections"]
    stages = []
    for index, item in enumerate(videos):
        attrs = " ".join(f'data-{key}="{escape(str(value), quote=True)}"' for key, value in {
            "video-stage": index, "src": item["src"], "poster": item["poster"],
            "title": item["title"], "description": item["description"],
            "duration": item["duration_seconds"],
        }.items())
        current = ' aria-current="step"' if index == 0 else ""
        stages.append(f'''<li><button class="video-step" type="button" {attrs}{current}
 aria-label="Video {index+1} of 3: {escape(item["title"])}">
<span class="video-step-number" aria-hidden="true">{index+1:02d}</span>
<span><span class="video-step-label">{escape(item["title"])}</span>
<span class="video-step-caption">{captions[index]}</span></span></button></li>''')
    body = header() + f'''<main class="page-shell video-layout video-story" id="main">
<div class="page-heading"><p class="eyebrow">PROJECT VIDEO</p>
<h1>The project in action</h1>
<p class="video-intro">Follow the journey from collecting road imagery to training the AI and detecting road defects.</p></div>
<nav aria-label="Project video stages"><ol class="video-steps">{''.join(stages)}</ol></nav>
<section class="video-card" aria-labelledby="video-title">
<div class="video-stage">
<video id="project-video-player" controls controlslist="nodownload" playsinline preload="metadata"
 src="{escape(first["src"])}" poster="{escape(first["poster"])}"
 aria-label="Data Collection — video 1 of 3">Your browser does not support HTML5 video.</video></div>
<div class="video-details"><div>
<p class="eyebrow" id="video-current-stage">STAGE 01 / 03</p>
<h2 id="video-title">{escape(first["title"])}</h2>
<p class="video-description" id="video-description">{escape(first["description"])}</p>
</div><span class="video-duration" aria-label="Video duration">
<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7.5" stroke="currentColor" stroke-width="1.4"/><path d="M10 5.5V10l3 2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
<span id="video-duration-text">{duration_label(first["duration_seconds"])}</span></span></div></section>
<p class="sr-only" id="video-status" role="status" aria-live="polite" aria-atomic="true"></p>
<div class="video-error" id="video-error" role="alert" hidden>
The video could not be loaded. Choose another stage, or <button id="video-retry" type="button">Try again</button>.</div>
<div class="video-follow-up">
<a class="video-button video-map-link" id="video-map" href="map.html" hidden>Explore Interactive Map →</a>
</div>
<noscript><style>.video-steps,.video-follow-up{{display:none}}</style>
<div class="video-no-script"><p>Enable JavaScript to switch between the three video stages.</p>
<a href="map.html">Explore Interactive Map →</a></div></noscript>
<nav class="page-footer" aria-label="Section navigation"><a href="index.html">← All sections</a><a href="map.html">Interactive map →</a></nav>
</main>'''
    return document("Project video", body).replace("</head>", '<link rel="stylesheet" href="css/video.css?v=20261026"><script src="js/video.js?v=20261026" defer></script></head>')

if __name__ == "__main__":
    from layout import document, header
    (SITE / "video.html").write_text(render_video(document, header), encoding="utf-8")
