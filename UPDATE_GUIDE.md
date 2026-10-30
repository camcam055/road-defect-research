# Website update guide

**Current reviewed revision: 30 October 2026. After local review, the owner approved pushing the report refresh and removal of Appendices A–D to the existing GitHub website. The repository and Pages URL remain unchanged. Future publication still requires the owner's instruction.**

The website is ready to serve from `site/`. It is a static GitHub Pages website: there is no database, login, build service or upload dashboard. Make changes to the files below, preview them, then upload/commit those files to your own repository when you choose to publish. The owner reviewed the 26 October 2026 report/map refresh and explicitly approved its commit, push and publication to the existing GitHub Pages URL. Future publication still requires the owner's instruction. The repository and Pages URL remain the same.

The owner reviewed and explicitly approved the 27 October 2026 corrections for commit, push and publication to the existing GitHub Pages URL. Future publication still requires the owner's instruction.

## Project video sequence

The Project Video page presents the final videos in this order:

1. **Data Collection** — source: `Updated data collection 01.mov`
2. **AI Training** — source: `02 AI training.mov`
3. **Road Defect Detection** — source: `03 Road defect detection.mov`

The website MP4s and matching JPG poster frames are listed in `site/data/videos.json`. All three stages use the replacement files supplied on 27 October 2026. They are silent H.264 video with the original dimensions and timing and fast-start metadata. The silent audio streams were removed at the owner's request. The original MOV files are preserved outside the website.

The maintained sequence and source checksums are in **`site/data/videos.json`**. **`tools/video_page.py`** renders the page; **`site/js/video.js`** and **`site/css/video.css`** supply its interactions and styling. The older single-video `SHOWCASE_CONFIG.videoSrc` setting is unused by this page.

Visitors select any of the three stage buttons above the video. Only one player loads a video at a time. Native controls provide play, pause, seeking and fullscreen. Volume controls and the native download option are hidden; `playsinline` supports mobile playback. The first video waits for Play. Selecting a stage while playing, or after a video finishes, starts the selected video following the visitor's click. Finishing a video marks its stage complete and highlights the next stage above the player; finishing the third reveals **Explore Interactive Map →**, linking to the existing `map.html`. Returning to an unfinished stage resumes its position for the current page session. Keyboard users can Tab to each stage or use Left/Right/Home/End within the stage controls. Reduced-motion preferences are respected.

To replace a video later, export a silent H.264 MP4 below GitHub's 100 MiB per-file limit, preserve the approved content, and use a new versioned asset name. Update the sequence's paths, poster, duration, dimensions, byte count and SHA-256 checksums, then run:

```sh
python3 tools/video_page.py
python3 tools/check_site.py
```

A normal `python3 tools/build_site.py` also regenerates the video page from this sequence. No original MOV, local filesystem path or private review record belongs in `site/`. Relative MP4/JPG URLs work under the existing GitHub Pages repository path, without Git LFS or an external media service.

The visible page keeps navigation above the player, without duplicate Previous/Next controls, direct MP4 links or playback guidance text. If playback fails, the error message offers Try again while preserving stage navigation. The native player uses controlslist=nodownload, hides volume controls, and suppresses its context menu; these are user interface choices, not copy protection. Browser-playable media can still be saved or captured by a determined visitor. With JavaScript disabled, the first native video remains available; switching stages requires JavaScript. Check playback, seeking and completion prompts at desktop and phone widths; a physical phone check remains useful before public release.

## Preview on your Mac

Unzip the package first. Double-click `Preview.command`, or open Terminal in the `research-showcase` folder and run:

```sh
python3 tools/preview.py
```

Open the printed localhost URL (normally `http://127.0.0.1:8766/`). Stop the server with Control+C. If macOS blocks the double-click launcher, run the Terminal command. Python 3 is needed for the preview and maintenance tools, but visitors need only a browser.

Use the local server for checking the map. The OpenFreeMap street basemap and OpenStreetMap fallback require internet. A local road network fallback is also included. The map libraries, marker icons, photos, glossary and report figures are bundled locally. The site works at a GitHub project URL such as `https://OWNER.github.io/REPOSITORY/` because internal paths are relative.

## Where things live

| What you want to update | File or folder |
| --- | --- |
| Research wording and result tables | `site/content/problem.html`, `methodology.html`, `literature-review.html`, `results.html`, `conclusion.html`, `future-work.html` |
| Bibliography | `site/content/references.html` |
| Research figures and chart exports | `site/assets/figures/` |
| Gallery photographs and actual annotated outputs | `site/assets/gallery/` |
| Gallery captions, filenames and saved prediction records | `site/data/gallery.json` |
| Glossary definitions, search aliases and source links | `site/data/glossary.json` |
| Interactive map and exported geographic data | `site/assets/map/index.html` |
| Map popup photos | `site/assets/map/images/` |
| Map mobile controls and basemap status | `site/assets/map/map-adapter.css`, `map-adapter.js` |
| Video sequence, provenance and posters | `site/data/videos.json` |
| Final video files and poster frames | `site/assets/video/` |
| Shared page navigation and homepage labels | `tools/layout.py` |
| General styling | `site/css/styles.css` |

## Update research text

For a small correction, edit the relevant HTML page in `site/content/` using a plain-text editor (VS Code, BBEdit, or TextEdit in plain-text mode). Find a distinctive phrase, change only the text inside its existing paragraph/heading/list item, and preserve its tags, `id` and `data-source-id` attributes. IDs support the table of contents and glossary source links. Escape a literal `&` as `&amp;` and `<` as `&lt;`. Save UTF-8 text.

The research pages reproduce the final report dated **30 October 2026**. The supplied PDF is the authoritative source. Its accompanying Word version was checked against the PDF before structured import. Keep future wording aligned with the report and record any intentional corrections. The public PDF hash, companion Word hash and import comparison are in `site/data/report-source.json`.

Website sections are 01 The Problem, 02 Literature Review, 03 Methodology, 04 Results, 05 Conclusion and 06 Future Work. Headings and contents use the website numbering; the research wording remains unchanged. Results omits its sample-photo and static-map appendices and their pointer sentence. Its findings, real-world testing and discussion remain. Appendices A–D have also been removed from Methodology, including their contents links and exclusive dataset-structure image. Parenthetical pointers to A and B and standalone pointers to other omitted appendices are excluded.

For an entire revised Word report, use the existing `tools/extract_report.py` importer. It needs `lxml` and `Pillow` and a reviewed, private content-plan JSON for that exact document. Keep the DOCX, plan and audit outside the website repository. Review section ranges, image identities, chart exports and privacy substitutions before importing; do not only replace the source hash. The importer rejects plans containing excluded front matter or administrative chapter material. Use the reviewed 30 October content plan; retain the standalone Future Work research. Keep its explicit exclusion ranges and two documented text replacements for pointers to removed appendices. When a new report changes body indices, remap the glossary source anchors and source-sensitive checks before regenerating pages. Record website heading-number substitutions in the plan. A fresh import overwrites manual changes in the research HTML pages. Run the importer again with `--verify-only` to compare source wording and equations. `tools/build_site.py` does not overwrite research paragraphs.

## Update images and figures

To replace a figure, export the correct figure from the report into `site/assets/figures/`, then change its `<img src="../assets/figures/NAME">` and surrounding full-size `<a href="...">` together. Update the `alt` description and the caption, including its source attribution. JPEG/PNG filenames are case-sensitive on GitHub Pages. Use genuine source figures and strip unneeded image metadata.

Native Word charts were exported from the report, rather than redrawn using poster values. When results change, re-export the corresponding chart and update both its caption and the accompanying result table/text. Keep labels, units and dataset descriptions legible on a phone.

## Update results

1. Use the authoritative report or actual evaluation export; open `site/content/results.html`.
2. Find the relevant heading and change the result text/table values together. Preserve the surrounding table tags and IDs.
3. Replace affected chart image exports and captions. Update related conclusions, glossary definitions and bibliography entries if the report changes them.
4. Keep sample sizes, validation conditions, limitations and the distinction between confidence and measured accuracy beside the results. The existing small New Zealand validation results do not establish dependable real-world performance.
5. Preview and run the checker below. Do not substitute poster dummy values or convert gallery examples into evaluation statistics.

## Update gallery images or detection examples

The gallery contains 18 reviewed labelled photographs grouped into longitudinal cracks, transverse cracks and alligator cracking. Sixteen have matching originals; two are labelled-only. Every card opens in AFTER mode.

Keep gallery assets in category subfolders under site/assets/gallery/. The maintained source is site/data/gallery.json (schema version 2). Each record needs a unique ID, primary category, source ID, AFTER filename/hash, display dimensions, annotations and a completed visible-box review. BEFORE is optional; use null when the original cannot be confirmed.

1. Use an existing saved labelled output with a visible road-defect box. Exclude raw standalone photos, zero-detection images, plots, mosaics, irrelevant boxes and duplicated exports. Do not fabricate detections to fill a category.
2. Confirm the source class-name mapping. Numeric IDs differ between historical runs and the current checkpoint. Record provenance per source; leave unavailable model details, raw coordinates or confidence values null.
3. Match BEFORE by source identity, orientation, aspect ratio and picture content. A similar filename is insufficient. Resize both views proportionally to identical dimensions and remove EXIF metadata. Keep only AFTER when there is no verified original.
4. Inspect the full annotated photograph and box detail at final display size. Record normalised review regions around real visible boxes. Set review.reviewed and review.visible_box true only after this inspection and update the review date.
5. Run python3 tools/refresh_gallery_hashes.py. Replacing either asset invalidates its prior review; inspect it again and restore review flags only when it passes.
6. Run python3 tools/build_site.py, python3 tools/check_site.py and python3 tools/verify_gallery_photos.py. The photo verifier requires Pillow; the build and static checker use the standard library.
7. Preview every new image, category filter, BEFORE/AFTER pair and full-size link. The build rejects an unfinished review, and the static checker rejects unused assets, duplicate images, missing box evidence, invalid mappings or unchanged unlabelled pairs.

A mixed-defect photograph appears once under its primary category, with all visible classifications retained in its annotation data and caption. See docs/GALLERY_REVIEW.md for this selection and docs/TRAINING_FILES_REVIEW.md for source limitations.

## Update the searchable glossary

Edit `site/data/glossary.json`. Each object inside `entries` has:

```json
{
  "term": "Example term (ABC)",
  "definition": "A concise explanation supported by your research.",
  "source": "methodology.html#b0898",
  "source_label": "Report §3.7",
  "aliases": "ABC alternative spelling related search words"
}
```

Use a unique term, valid JSON commas/quotes and a working source link. Source links are relative to `site/content/glossary.html`. `aliases` helps searches find abbreviations and alternative spellings; it is not shown as definition text. Entries appear in JSON order; keep them alphabetical. Then run:

```sh
python3 tools/build_sections.py
python3 tools/check_site.py
```

JSON edits alone do not change the rendered page: the first command regenerates the static HTML. Search is case-insensitive, handles common accents/hyphens, and matches all words typed across terms, aliases and definitions. All entries remain readable with JavaScript disabled.

## Update map data

The map fills the first viewport and has one Back link. Exploring Potential Relationships follows directly underneath. The map's controls, legends and provider attribution remain available. All defect runs share a single Road defects switch, and run identities remain in the popups.

All saved run folders are retained in the export. All runs with usable GPS are visible by default through the unified Road defects switch. Per-run counts and owner exclusions are in `site/data/map-source.json`. The CSV uses `map_display_status` to distinguish mapped records, unavailable GPS and owner-requested exclusions. Run6 IMG_6869, IMG_6871 and IMG_6872 are excluded from the map; their original detection records are retained.

Keep `master_defect_map.html` with its `master_defect_map_assets/` folder outside the repository. A current application export can place its assets inside a versioned build directory identified by the HTML metadata. It includes `observations.csv` and `run_coverage.json` and applies its persistent display-exclusion list. After reviewing the export, run `python3 tools/import_portable_map.py --source PATH_TO_HTML --audit PRIVATE_AUDIT_DIRECTORY`. Back up the public map first and keep the audit outside this repository.

The importer copies every referenced photograph from the master export, including annotated images stored in run folders, the observation CSV and bundled vendor files. It removes private image metadata without changing pixels and checks the complete map against the source after relative paths and the separate website adapter. It compares the marker count with the all-run coverage record. Original reports, source manifests and private reviews stay outside Git.

The website supplies the Back link in its full-page map. The separate map adapter supplies Back when the map is opened directly and keeps controls clear of narrow-screen popups. Version queries refresh the map and its changed CSS/JavaScript while retaining the public root address.

Check desktop and phone sizes, earlier-run markers, density/layer controls and Back/homepage navigation before deployment. Keep observations, marker groups, missing GPS, display exclusions and density assessments distinct.

## Checks after an update

```sh
python3 tools/check_site.py
```

This checks all HTML/CSS local links, source anchors, the ten homepage cards, gallery file hashes, class mappings, visible-box review records, optional originals and bounding-box ranges, JSON structure, private-path leaks, bundled map libraries and the manual Pages workflow. It is not a statistical validation of a new model or dataset.

Preview desktop and phone widths. Check all section links, gallery switches/full-size images, glossary search/clear/no-results, readable tables and figures, map tiles/popups/layers, and the three final videos, including end-of-video prompts. Check the final MP4s on a physical phone before release. See `docs/VERIFICATION.md` for the delivered build's actual test coverage and limits.

## GitHub Pages deployment when you are ready

The package contains the existing repository layout: `site/` is the public document root, and `.github/workflows/pages.yml` publishes that folder. You can upload the unzipped files to your repository without Python build steps because the HTML is already generated. Keep `.github/` and `tools/check_site.py` with the repository; exclude `.git/`, private reports and audit folders.

1. In your repository, set **Settings → Pages → Source → GitHub Actions**.
2. Ensure the files are on the `main` branch. In **Actions**, choose **Publish approved showcase → Run workflow** and tick its publication approval input only when you want it public.
3. The workflow runs the checker and uploads only `site/`. It has no push-triggered deployment.
4. Open the HTTPS URL reported by the deployment and check it anonymously. Updating a video, image or text file still requires rerunning the workflow.

Alternative: if you already use **Deploy from a branch**, copy the *contents* of `site/` to that branch's configured root (including `.nojekyll`) and use that normal Pages process. Do not point branch deployment at this package's repository root, which contains maintenance files rather than the website's `index.html`.

The existing Pages workflow remains manual. Each requested public update requires its publication approval input; the repository name and current URL are retained.
