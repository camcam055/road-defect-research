**The owner approved this reviewed report update for the existing GitHub Pages website on 30 October 2026.**

# Road defect research showcase

Completed static companion to Campbell Searle’s MG7101 engineering research. The existing design is retained: two featured cards, followed by research sections 01–08. Section 07 contains 76 reviewed labelled photographs grouped by defect category, with 74 independent BEFORE/AFTER pairs and two labelled-only examples; Section 08 contains 46 source-linked, searchable definitions.

Research text and figures use the final report dated 30 October 2026. The supplied PDF is the authoritative source, with its accompanying Word version checked against it for structured import. Appendices A–D and their exclusive assets have been removed, and prior administrative and report-only exclusions are preserved. Source wording, preliminary-result limitations, original chart data and bibliography gaps are retained honestly. Project Video now presents the three final owner-supplied videos in order: Data Collection, AI Training and Road Defect Detection, with manual stage selection, next-stage completion highlights and a final link to the interactive map. Browser-compatible MP4 copies retain the original dimensions and timing; original MOV files remain unchanged.

Live website: [Road defect research](https://camcam055.github.io/road-defect-research/).

## Use and update

Start with **UPDATE_GUIDE.md**, including the project video sequence instructions. Double-click Preview.command, or run `python3 tools/preview.py`. Only site/ is served. The map fills the first viewport with a single Back link, followed directly by Exploring Potential Relationships. All available runs share one Road defects toggle. The latest supplied master export contains 508 markers representing 580 displayed observations. The CSV retains all 721 records across 12 runs, including 137 without usable GPS and four records covered by the existing run6 display exclusions. Street basemaps need internet; map libraries, all 524 referenced photographs, observation CSV and a local road fallback are bundled.

The website is ready to deploy without a framework or build step. The manual GitHub Pages workflow publishes site/ only and requires its publication approval input.

## Maintenance commands

```sh
python3 tools/build_site.py
python3 tools/check_site.py
```

The build command regenerates shared navigation, the gallery and glossary. It preserves existing research HTML. The separate DOCX importer needs a reviewed private source plan, lxml and Pillow; neither original reports nor model weights are required to serve the site.

See docs/GALLERY_REVIEW.md for photo selection and docs/TRAINING_FILES_REVIEW.md for application reuse findings. See docs/VERIFICATION.md and docs/VIDEO_VERIFICATION.md for observed browser checks and limitations. Public provenance: site/data/report-source.json, site/data/map-source.json and site/data/gallery.json. Keep original PDF/Word/PowerPoint files, model checkpoints, private source mappings and review records outside this repository.
