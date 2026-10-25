# Website update guide

The website is ready to serve from `site/`. It is a static GitHub Pages website: there is no database, login, build service or upload dashboard. Make changes to the files below, preview them, then upload/commit those files to your own repository when you choose to publish. The 25 October 2026 report/map refresh is prepared for the owner's requested update to the existing GitHub Pages site. The repository and Pages URL remain the same.

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
| Video path and optional poster | `site/js/config.js` |
| Video file | `site/assets/video/project-demo.mp4` |
| Shared page navigation and homepage labels | `tools/layout.py` |
| General styling | `site/css/styles.css` |

## Update research text

For a small correction, edit the relevant HTML page in `site/content/` using a plain-text editor (VS Code, BBEdit, or TextEdit in plain-text mode). Find a distinctive phrase, change only the text inside its existing paragraph/heading/list item, and preserve its tags, `id` and `data-source-id` attributes. IDs support the table of contents and glossary source links. Escape a literal `&` as `&amp;` and `<` as `&lt;`. Save UTF-8 text.

The research pages reproduce the latest supplied report saved on **25 October 2026**. Its cover is labelled Final Report; its supplied filename retains draft. Keep future wording aligned with the report and record any intentional corrections. The public source hash and import comparison are in `site/data/report-source.json`.

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

The current map is the portable export saved on 25 October 2026. It retains the source's grouped observations, recovered density, historical observations, overlays, basemap fallbacks and uncertainty notes. Public provenance is in `site/data/map-source.json`. The observation CSV is linked from the map.

Keep a revised `master_defect_map.html` together with its `master_defect_map_assets/` folder outside the repository. After reviewing the source and referenced photos, run `python3 tools/import_portable_map.py --source PATH_TO_HTML --audit PRIVATE_AUDIT_DIRECTORY`. The audit directory must be outside this repository. The importer copies referenced images, the observation CSV and bundled vendor files, removes image metadata and preserves the complete map after documented relative-path and navigation additions. Source manifests and private review records stay outside Git. Back up the existing public map before import.

The portable export has its own responsive controls and basemap fallbacks. The separate map adapter supplies the Home link, accessibility label and loading-status messages. On narrow screens, the inspection panel and layers control are hidden while a popup is open so its photo and close control remain accessible. Closing the popup restores them.

Run the static checks, preview the embedded and full-size map, open a defect photo, toggle density/overlay controls, and check a phone-width viewport before deployment. Preserve the distinction between tentative grouped locations, located observations, observations without GPS and assessable road sections.

## Checks after an update

```sh
python3 tools/check_site.py
```

This checks all HTML/CSS local links, source anchors, the ten homepage cards, gallery file hashes, class mappings, visible-box review records, optional originals and bounding-box ranges, JSON structure, private-path leaks, bundled map libraries and the manual Pages workflow. It is not a statistical validation of a new model or dataset.

Preview desktop and phone widths. Check all section links, gallery switches/full-size images, glossary search/clear/no-results, readable tables and figures, map tiles/popups/layers, and your video once it is available. Test the final MP4 on a physical iPhone when you have it. See `docs/VERIFICATION.md` for the delivered build's actual test coverage and limits.

## GitHub Pages deployment when you are ready

The package contains the existing repository layout: `site/` is the public document root, and `.github/workflows/pages.yml` publishes that folder. You can upload the unzipped files to your repository without Python build steps because the HTML is already generated. Keep `.github/` and `tools/check_site.py` with the repository; exclude `.git/`, private reports and audit folders.

1. In your repository, set **Settings → Pages → Source → GitHub Actions**.
2. Ensure the files are on the `main` branch. In **Actions**, choose **Publish approved showcase → Run workflow** and tick its publication approval input only when you want it public.
3. The workflow runs the checker and uploads only `site/`. It has no push-triggered deployment.
4. Open the HTTPS URL reported by the deployment and check it anonymously. Updating a video, image or text file still requires rerunning the workflow.

Alternative: if you already use **Deploy from a branch**, copy the *contents* of `site/` to that branch's configured root (including `.nojekyll`) and use that normal Pages process. Do not point branch deployment at this package's repository root, which contains maintenance files rather than the website's `index.html`.

The existing Pages workflow remains manual. Each requested public update requires its publication approval input; the repository name and current URL are retained.
