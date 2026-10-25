# Road defect research showcase

Completed static companion to Campbell Searle’s MG7101 engineering research. The existing design is retained: two featured cards, followed by research sections 01–08. Section 07 contains 18 reviewed labelled photographs grouped by defect category, with 16 independent BEFORE/AFTER pairs and two labelled-only examples; Section 08 contains 46 source-linked, searchable definitions.

Research text and figures use the latest supplied report saved on 25 October 2026. Its cover is labelled Final Report; its supplied filename retains draft. Source wording, preliminary-result limitations, original chart data and bibliography gaps are retained honestly. The video placeholder is intentional: the owner will supply the final MP4 later.

Live website: [Road defect research](https://camcam055.github.io/road-defect-research/).

## Use and update

Start with **UPDATE_GUIDE.md**, including the short video upload instructions. Double-click Preview.command, or run `python3 tools/preview.py`. Only site/ is served. The updated map includes 2,491 tentative run16 defect locations, 2,977 located observations and recovered section density. Street basemaps need internet; map libraries, 1,902 referenced photographs, observation CSV and a local road fallback are bundled.

The website is ready to deploy without a framework or build step. The manual GitHub Pages workflow publishes site/ only and requires its publication approval input.

## Maintenance commands

```sh
python3 tools/build_site.py
python3 tools/check_site.py
```

The build command regenerates shared navigation, the gallery and glossary. It preserves existing research HTML. The separate DOCX importer needs a reviewed private source plan, lxml and Pillow; neither original reports nor model weights are required to serve the site.

See docs/GALLERY_REVIEW.md for photo selection and docs/TRAINING_FILES_REVIEW.md for application reuse findings. See docs/VERIFICATION.md for observed browser checks and limitations. Public provenance: site/data/report-source.json, site/data/map-source.json and site/data/gallery.json. Keep original Word/PowerPoint files, model checkpoints, private source mappings and review records outside this repository.
