# Report and map refresh verification - 25 October 2026

The owner requested updating the existing website and GitHub repository while retaining https://camcam055.github.io/road-defect-research/. The local checkout was clean at the existing published revision before this refresh. The repository identity and manual Pages workflow are preserved.

- Seven research/reference pages reproduce 304 nonblank source blocks from the revised report after the four existing privacy substitutions. Equations match the source. The five native chart XML files match the preceding source; all 21 current report figure/chart assets are retained.
- The conclusion and proposed sensor work are updated. The repeated section 3.7 LLM proposal is retained in Methodology and appears once in Future Work under section 5.2. The glossary has 46 terms, with source anchors remapped to the revised report.
- The portable map is preserved in full after relative asset paths, a title and the separate website adapter. It contains 2,491 tentative run16 defect locations, 2,977 located observations and 21 observations without GPS, plus 22 historical markers. Grouping qualifications and the separate recovered-density layer are retained.
- All 1,902 referenced map photographs passed pixel-preserving metadata removal. The 2,998-row observation CSV and bundled vendor files/licences are included. Original reports, source manifests and private audits remain outside the repository.
- In the in-app browser at 475px width, the homepage, updated conclusion, future-work text, glossary search and sensor source link worked without document-level horizontal overflow.
- Embedded and full-size maps loaded. OpenFreeMap and the OSM fallback rendered; clusters zoomed, latest/recovered density and historical layers toggled, and a new run16 popup photograph loaded at 960px source width. Popup close restored the controls. On narrow screens the adapter hides the information/layer panels while a popup is open to keep its photo and close control accessible.
- The original gallery data/assets, homepage card order, visual design and video configuration remain intact. The final MP4 is still an intentional placeholder.

Final checks: static validation PASS (13 HTML documents, 10 homepage cards, 8,372 local references including observation photos); source comparison PASS (304 blocks and equations); Python syntax PASS (13 maintenance scripts); map adapter JavaScript syntax PASS; source hashes, unchanged gallery/video assets and map canonical comparison PASS. MANIFEST.sha256 is regenerated and verified. Narrow-screen checks use a desktop app browser panel, not a physical iPhone. External basemap availability depends on network access. The map is a research demonstration; its observations do not establish measured detection accuracy.

---

# Earlier verification snapshots

The following entries describe earlier revisions and are retained as historical records.

# Gallery refresh verification - 23 October 2026

The photo organisation and gallery update were completed and tested locally before the owner's authorised GitHub commit, push and existing Pages deployment.

- Reviewed 128 saved exports and checked the 71-photo source collection for matching originals.
- Selected 18 annotated photographs: 11 longitudinal-crack, five transverse-crack and two alligator-cracking examples. Sixteen have verified originals; two are labelled-only.
- Each selected AFTER image passed whole-photo and box-detail visual inspection and a coloured box-border check on its final JPEG. All 34 JPEG files passed integrity, dimensions, hash and EXIF-removal checks.
- Browser at 1280px desktop width: all four filters return the expected counts; all 16 pairs passed both modes (32 checks), with independent state and correct full-size targets. All 34 image elements decoded successfully.
- Browser at 390px phone width: one-column layout, no document-level horizontal overflow, category filtering and independent image switching work. Complete image containment was verified for all 18 annotated photographs at both widths, including the portrait-image CSS correction.
- The two labelled-only cards load without misleading BEFORE controls. A labelled-only full-size image was opened successfully.
- No application-origin warning/error messages were observed in the gallery browser console.
- Static site checker: PASS, 13 HTML documents, 10 homepage cards and 401 local references. JavaScript syntax: PASS.
- Original research text, glossary, homepage, map content/assets, video configuration and the application's detection model were preserved. Detailed local review evidence and screenshots remain outside Git.

The phone-width checks use a desktop browser viewport, not a physical iPhone. This remains a curated visual gallery, not an independent model accuracy evaluation. Historical source/model details unavailable in the saved exports are left unknown.

---

## Previous delivered verification snapshot

The following records the preceding package's checks. Its three-image gallery and no-detection example have been superseded by the reviewed refresh above.

# Delivered website verification

Checked 23 October 2026 (Pacific/Auckland). The package was prepared locally; no GitHub push, publication or external hosting registration occurred.

## Browser checks

| Browser / view | Observed result |
| --- | --- |
| macOS Safari, desktop | Homepage navigation and independent gallery BEFORE/AFTER switches work; genuine annotated photographs and full-size links render. |
| macOS Safari Responsive Design Mode, 390 × 844 | Gallery switching, glossary filtering (`pDi`), Clear restoring 44 entries, and no-results state work. |
| Safari phone-size map view | Live OpenStreetMap basemap renders. Map layers and soil legend expand/collapse; a traffic layer toggles; zoom and defect clusters work; a defect photo popup renders its image and has a reachable close control. |
| Chrome, 375 × 812 | All 12 primary website pages load with no document-level horizontal overflow. Tables retain their own horizontal scrolling. |
| Chrome, 1280 × 900 | All 12 primary pages load with no document-level horizontal overflow. No application-origin console errors observed. |
| Chrome gallery / glossary interactions | All three image pairs switch correctly, one card does not change another, full-size links follow the selected mode, search finds PDI case-insensitively, no-results and Clear work. |
| Chrome map | 18 live OpenStreetMap tile images loaded successfully at 256 × 256; the basemap state was `loaded` and the parent loading message disappeared. |

The Safari mobile-width checks use desktop Safari’s Responsive Design Mode, not a physical iPhone or an iOS Simulator. Hardware-specific touch/rotation and the final video's playback should be checked on the owner's phone when the MP4 is available. The native HTML5 video controls and intentional placeholder are included; no final video was supplied or fabricated.

## Source and file checks

- Latest supplied report hash matches the current source document saved on 22 October 2026: `0235bb32ca5a71e6a44a4c6d6dbaf586c36847e0148116d420d880d089ae1365`.
- Seven research/reference pages compared against the source: 301 nonblank mapped blocks match after four documented privacy replacements. Equations also match. Original native chart sources were unchanged; 21 current figure/chart assets are included.
- Gallery source photograph hashes and the original project checkpoint hash verified. Saved prediction coordinates/confidences retained; the no-detection example uses byte-identical BEFORE/AFTER images.
- Static checker passes: 13 HTML documents (including the nested map), 10 homepage cards and 359 local HTML/CSS references.
- JavaScript syntax passes for 12 bundled/inline scripts; Python syntax passes for all 9 maintenance scripts; 73 raster images pass image-integrity checks.
- Map libraries, icons and fonts are bundled. Basemap tiles are live requests requiring internet; no API key or tile archive is included.
- Oversized map popup photos replaced only in the website with proportional web-sized copies. Original photographs remain outside the website, and existing privacy-withheld placeholders remain.
- ZIP archive CRCs and extracted-package static validation checked before delivery. Package file hashes are listed in MANIFEST.sha256.

## Research and owner follow-up

The authoritative source remains labelled as a draft. Its small-sample/generalisation caveats and unresolved bibliography/count/parameter inconsistencies are retained rather than inventing corrections. Gallery confidence values are not evaluation accuracy.

The final MP4 is intentionally left for the owner to add. UPDATE_GUIDE.md gives the exact upload folder, filename, video configuration, troubleshooting and future content-update steps. Deployment is manual and remains the owner's choice.
