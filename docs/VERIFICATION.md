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
