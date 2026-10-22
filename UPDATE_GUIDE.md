# Website update guide

The website is ready to serve from `site/`. It is a static GitHub Pages website: there is no database, login, build service or upload dashboard. Make changes to the files below, preview them, then upload/commit those files to your own repository when you choose to publish. Nothing was pushed or published during this development session.

## Add your video — the short version

1. Export the final video as **MP4 with H.264 video and AAC audio**. This format works in Safari. Name it **`project-demo.mp4`** (lowercase, no spaces).
2. Put it in **`site/assets/video/project-demo.mp4`**. On GitHub, open the repository folder `site/assets/video`, select **Add file → Upload files**, and upload the MP4 there.
3. Open **`site/js/config.js`** and change the configuration to:

   ```js
   window.SHOWCASE_CONFIG = {
     videoSrc: "assets/video/project-demo.mp4",
     videoPoster: ""
   };
   ```

   In GitHub, use the pencil icon to edit that file and save the change. The path is relative to `video.html`; do not add `site/` at the start of `videoSrc`.
4. Preview `video.html`, or redeploy your Pages site after saving both files. Check play, pause, seeking, sound, fullscreen and rotation in Safari. The player uses native controls and `playsinline`; it does not autoplay.

That is all: **one MP4 upload and one configuration edit**. There is no need to change HTML or install video software on the website. Until the MP4 is supplied, the intentional placeholder stays visible.

Optional: put a poster frame at `site/assets/video/poster.jpg` and set `videoPoster: "assets/video/poster.jpg"`. For practical mobile loading, use 1080p and a sensible bitrate. Keep each Git file below GitHub's 100 MiB file limit. If needed, export a smaller MP4 or set `videoSrc` to a direct public HTTPS MP4 URL that permits playback; a YouTube watch-page URL is not an MP4 source. Do not commit raw camera footage or credentials.

If the player shows an error: check spelling/capitalisation of the filename, confirm the MP4 is in the published `site/assets/video/` folder, and verify its H.264/AAC encoding. Set `videoSrc` back to `""` to restore the placeholder.

## Preview on your Mac

Unzip the package first. Double-click `Preview.command`, or open Terminal in the `research-showcase` folder and run:

```sh
python3 tools/preview.py
```

Open the printed localhost URL (normally `http://127.0.0.1:8766/`). Stop the server with Control+C. If macOS blocks the double-click launcher, run the Terminal command. Python 3 is needed for the preview and maintenance tools, but visitors need only a browser.

Use the local server for checking the map. Live OpenStreetMap tiles require internet. The map libraries, marker icons, photos, glossary and report figures are bundled locally. The site works at a GitHub project URL such as `https://OWNER.github.io/REPOSITORY/` because internal paths are relative.

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
| Map popup photos | `site/assets/map/photos/` |
| Map mobile controls and basemap status | `site/assets/map/map-adapter.css`, `map-adapter.js` |
| Video path and optional poster | `site/js/config.js` |
| Video file | `site/assets/video/project-demo.mp4` |
| Shared page navigation and homepage labels | `tools/layout.py` |
| General styling | `site/css/styles.css` |

## Update research text

For a small correction, edit the relevant HTML page in `site/content/` using a plain-text editor (VS Code, BBEdit, or TextEdit in plain-text mode). Find a distinctive phrase, change only the text inside its existing paragraph/heading/list item, and preserve its tags, `id` and `data-source-id` attributes. IDs support the table of contents and glossary source links. Escape a literal `&` as `&amp;` and `<` as `&lt;`. Save UTF-8 text.

The research pages reproduce the latest supplied report saved on **22 October 2026**. That document is still labelled as a draft. Keep future wording aligned with the report and record any intentional corrections. The public source hash and import comparison are in `site/data/report-source.json`.

For an entire revised Word report, use the existing `tools/extract_report.py` importer. It needs `lxml` and `Pillow` and a reviewed, private content-plan JSON for that exact document. Keep the DOCX, plan and audit outside the website repository. Review section ranges, image identities, chart exports and privacy substitutions before importing; do not only replace the source hash. A fresh import overwrites manual changes in the research HTML pages. Run the importer again with `--verify-only` to compare source wording and equations. `tools/build_site.py` does not overwrite research paragraphs.

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

The three delivered examples use saved inference from the project checkpoint on **22 October 2026**, with `imgsz=960`, `conf=0.40` and `iou=0.70`. The checkpoint hash, software versions, image hashes, class IDs, confidence values and original bounding-box coordinates are retained in `site/data/gallery.json`. Two examples contain real model predictions; the third honestly shows a visible crack for which the model returned no detection. The annotations are visualisations of saved predictions, not manually invented detections.

For a replacement or new example:

1. Run the actual project YOLO checkpoint on the original photo and retain the actual inference output. Export the unannotated photo and the annotated output with the same orientation, crop and display dimensions. Resize both proportionally if needed; do not move or redraw detections to make them look better. For a no-detection example, use identical before and after files.
2. Put the display files in `site/assets/gallery/`, for example `example-04-before.jpg` and `example-04-after.jpg`. Remove EXIF metadata before including new photos and check for personal details.
3. Duplicate an image record in `site/data/gallery.json`. Give it a unique `id`, a `title`, the two filenames, original `width`/`height`, and display `display_width`/`display_height`. Paste its genuine `predictions` (`class_id`, `class_name`, `confidence`, pixel `xyxy`, normalised `xyxyn`) and source hash. An empty list means no detection. The top-level model/options must describe the run used for all displayed examples; rerun all selected examples if changing the checkpoint or settings.
4. Run:

   ```sh
   python3 tools/refresh_gallery_hashes.py
   python3 tools/build_sections.py
   python3 tools/check_site.py
   ```

5. Open Section 07. Test BEFORE and AFTER for every example, including the no-detection case and full-size links.

The website displays precomputed output; it does not run YOLO in visitors' browsers. Keep model weights and private inference inputs outside the website package.

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

The map is a saved Folium/Leaflet export. Geographic features, layer names, traffic values, soils and defect-section data are embedded in `site/assets/map/index.html`. This file is not generated from the glossary or gallery.

1. Generate a new map from the actual project inspection outputs. Preserve coordinate systems, count definitions and documented limitations. Work on a copy; do not edit or round coordinates merely to change the display.
2. Replace the exported map and its associated popup photos. Photos must be web-relative, such as `photos/photo-001.jpg`; `file:///` links and private computer paths will not work on GitHub Pages. For an export containing local photo links, use the provided importer:

   ```sh
   python3 tools/import_map.py --source "/path/to/new-map.html" --output site/assets/map --audit "/path/to/private-map-audit" --openstreetmap-basemap
   ```

   The importer needs Pillow and lxml. Add `--withhold FILENAME` for any source photo that should stay withheld. Keep the current three withheld images unless you have reviewed replacement photos. The importer changes display/asset paths, not research coordinates or values.
3. Retain `map-adapter.css` in the map `<head>` and `<script src="map-adapter.js" defer></script>` after the generated map script. Retain the existing local `vendor/` directory. For a freshly exported map with CDN script links, run:

   ```sh
   python3 tools/bundle_map_assets.py
   ```

   This downloads the referenced library assets and rewrites them to local paths. Internet is needed for that preparation step. A new library dependency requires checking its license and adding its notice to `vendor/`.
4. The basemap URL is **`https://tile.openstreetmap.org/{z}/{x}/{y}.png`**, with OpenStreetMap attribution and native tile zoom limited to 19. It requires no API key. Keep attribution visible. Do not add API credentials to a static website or bundle/download a region of tiles for offline use.
5. Use web-sized copies of popup photos (up to about 1800 pixels on their longest side). Preserve the original photographs privately. This avoids loading full camera originals on phones. Keep detections and any existing annotation geometry aligned when resizing.
6. Change the iframe version in `tools/layout.py` (the `?v=...` value) when replacing a released map, then run `python3 tools/build_site.py`. Remove superseded public photos only after confirming the new links and privacy review.
7. Preview `map.html` and the **Open map** link. Wait for actual street/land/water tiles to appear, zoom in/out, pan, toggle layers, open a defect photo popup and check both legends. On a phone-width view, use **Map layers** and **Soil legend**. A tile failure displays a retry message rather than pretending the basemap loaded.

## Checks after an update

```sh
python3 tools/check_site.py
```

This checks all HTML/CSS local links, source anchors, the ten homepage cards, gallery file hashes and bounding-box ranges, JSON structure, private-path leaks, bundled map libraries and the manual Pages workflow. It is not a statistical validation of a new model or dataset.

Preview desktop and phone widths. Check all section links, gallery switches/full-size images, glossary search/clear/no-results, readable tables and figures, map tiles/popups/layers, and your video once it is available. Test the final MP4 on a physical iPhone when you have it. See `docs/VERIFICATION.md` for the delivered build's actual test coverage and limits.

## GitHub Pages deployment when you are ready

The package contains the existing repository layout: `site/` is the public document root, and `.github/workflows/pages.yml` publishes that folder. You can upload the unzipped files to your repository without Python build steps because the HTML is already generated. Keep `.github/` and `tools/check_site.py` with the repository; exclude `.git/`, private reports and audit folders.

1. In your repository, set **Settings → Pages → Source → GitHub Actions**.
2. Ensure the files are on the `main` branch. In **Actions**, choose **Publish approved showcase → Run workflow** and tick its publication approval input only when you want it public.
3. The workflow runs the checker and uploads only `site/`. It has no push-triggered deployment.
4. Open the HTTPS URL reported by the deployment and check it anonymously. Updating a video, image or text file still requires rerunning the workflow.

Alternative: if you already use **Deploy from a branch**, copy the *contents* of `site/` to that branch's configured root (including `.nojekyll`) and use that normal Pages process. Do not point branch deployment at this package's repository root, which contains maintenance files rather than the website's `index.html`.

No automatic publishing, GitHub push or external hosting registration was performed to create this package.
