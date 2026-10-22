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
