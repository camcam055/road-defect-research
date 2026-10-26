# Local website review — 26 October 2026

At completion of this local review, no Git commit, push, publication, Pages deployment or GitHub workflow had been performed. The owner subsequently approved publication to the existing repository and website URL.

## Research and privacy

Sections 01–06 and the references page reproduce the latest supplied report. Per-block source comparison passed for 326 nonblank blocks after the four existing privacy substitutions, with equations checked separately. Final model performance, real-world testing, discussion, conclusion and future work are included. The Executive Summary is excluded completely. The report's original wording, numerical claims, qualifications and numbering are retained.

All 30 referenced report figure/chart assets are included. The three new performance charts were rendered from the native Word chart objects; the five earlier native chart sources are unchanged. The 46 glossary definitions are preserved and their report links have been remapped.

## Master map and requested combined layer

The latest supplied master export contains 508 markers representing 580 mapped observations, with 721 exported records across 12 runs. It retains 137 records without usable GPS and the four records associated with the three existing run6 display exclusions.

The imported map HTML and observation CSV match the master after controlled relative-path and website-adapter additions. All PDI visualisations, traffic corridors and stations, soil polygons, road network, marker clusters, images and popup metadata are retained. All 524 referenced photographs passed pixel-preserving metadata removal. All 542 local map runtime/photo/CSV references returned HTTP 200 during verification.

The owner requested combining the separate run controls. The exported map now creates one enabled Road defects switch for all runs before its layer menu is rendered. The old run-specific labels are removed from the exported HTML. Switching it off hides the markers; switching it on restores them. The master map and detection application remain unchanged.

Exploring Potential Relationships appears directly below the map, using the supplied text and matching typography, colours and spacing. Three cards display in a row on desktop and a single column on phone widths. Narrow-screen popup controls no longer cover the popup title or photo.

## Observed local checks

- Static site checks: PASS, 13 HTML pages, 10 homepage cards, no missing local links or source anchors, no private filesystem paths, and no excluded front matter.
- Exact report wording and equation comparison: PASS.
- Master-map HTML/data preservation and all referenced map HTTP assets: PASS.
- JavaScript and Python helper syntax checks: PASS.
- All six research pages: no horizontal page overflow at 390 × 844 and 1280 × 900.
- Map: primary OpenFreeMap street rendering, local-road fallback, all traffic/soil/road/PDI switches, combined defect switch, zoom/cluster expansion, desktop and phone popups, and loaded popup photographs checked.
- Gallery: all 76 entries retained; BEFORE/AFTER and full-size image links work; Potholes filter shows three entries.
- Glossary: 46 entries retained; search, no-results and Clear checked.
- Project videos: existing three files and controls preserved; native playback starts and all three stage selectors load valid durations without media errors.
- Homepage card order, navigation, existing root entry used by the NFC poster and manual publication workflow are preserved.

Physical phone hardware and a physical NFC tap were not tested. Phone checks use the desktop app browser viewport. Online street basemaps still depend on an internet connection.

## Local review

Open http://127.0.0.1:8766/ while the local preview is running. The map is at http://127.0.0.1:8766/map.html?v=20261026-final.

If needed, restart it with Preview.command or python3 tools/preview.py. The preview serves only site/ and binds to this computer.

The complete list of files changed during this update, compared with the pre-existing local working tree, is in LOCAL_FILE_CHANGES_20261026.json. Existing uncommitted gallery/video work was retained.
