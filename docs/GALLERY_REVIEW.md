# Curated road-defect gallery

Reviewed 23 October 2026 before updating the gallery page.

## Inspection and selection

The review covered 128 saved image exports across the organised training predictions, current and historical application outputs, video outputs and existing map photographs. The 71-photo source collection was checked for original matches. Repeated map copies and adjacent video-frame variants were reviewed together.

Selected: 18 labelled images, consisting of 16 confirmed BEFORE/AFTER pairs and two labelled-only exports.

| Primary category | Photos |
| --- | ---: |
| Longitudinal cracks | 11 |
| Transverse cracks | 5 |
| Alligator cracking | 2 |

A photo showing both transverse and longitudinal cracks appears once in the transverse group, with both classifications retained in its title and annotation data. No unverified pothole or other-defect example was added merely to populate a category.

## Acceptance checks

Each selected AFTER image was inspected as a whole photograph and in a box-detail view. A separate check detects coloured border pixels in the recorded review regions at the final JPEG display size. Saved annotations were retained; boxes and confidence values were not invented or regenerated.

For paired photographs, source identity, EXIF orientation, aspect ratio and image-content comparison were checked before proportional resizing. A visually similar roadway image failed content matching and was retained without a BEFORE image. No original was guessed from a filename alone.

The dedicated website directory is site/assets/gallery/, with one subdirectory per category. The manifest is site/data/gallery.json. Images are proportionally resized to a maximum 1600 pixels per side and exported without EXIF metadata. The default view is AFTER.

## Exclusions and provenance

Excluded items include unlabelled exports, the former no-detection gallery example, a former prediction boxing a leaf, phone screenshots, sideways video exports, ambiguous/conflicting detections, irrelevant training plots and mosaics, and duplicate or near-duplicate exports. The country-prefixed source collection previously removed by the owner was not reintroduced.

The public manifest contains per-source class mappings, asset hashes, available sidecar annotations, pairing checks and visible-box review regions. Missing raw coordinates, confidence values, checkpoint identities or source thresholds remain null. Historical examples are not represented as current-model output. Detailed local source paths and the full exclusion log remain in the private review area.

These are curated saved model annotations, not ground truth, independent validation, repair advice or accuracy measurements.
