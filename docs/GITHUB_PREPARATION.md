# GitHub delivery preparation

Repository: camcam055/road-defect-research

Existing website URL: https://camcam055.github.io/road-defect-research/

The owner authorised updating this existing repository and live GitHub Pages site after local photo organisation and gallery verification. The work is prepared on gallery/reviewed-defect-photos and will be integrated into the existing main branch, committed and pushed through the existing checkout. No new repository or website URL is required.

Commit title: Curate labelled road defect gallery by category

Verified before delivery:

- 18 reviewed labelled photos, 16 confirmed pairs, two labelled-only examples.
- All 34 gallery JPEGs load and pass integrity, metadata-removal and box-evidence checks.
- All category filters and all 32 pair modes work in the browser.
- Desktop and phone-width image containment, layout and independent controls pass.
- Static site checks and JavaScript syntax pass; research/map/glossary content is preserved.

The existing manual GitHub Pages workflow is used with the owner's publication approval. Model weights, private source mappings and local review records remain outside the repository. The Desktop research-showcase package is synchronised with the verified implementation.

For future updates run python3 tools/build_site.py, python3 tools/check_site.py and python3 tools/verify_gallery_photos.py (Pillow required for the last command). Repeat browser/photo review when assets or behaviour change.
