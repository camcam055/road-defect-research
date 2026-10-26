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

## Run2 gallery extension - 26 October 2026

Added all 16 eligible saved annotated video frames from run2, each paired with its exact unannotated frame from the source-video frame manifest. All 18 existing entries and 34 existing gallery image files are preserved. The gallery now contains 34 entries: 32 BEFORE/AFTER pairs and two existing labelled-only examples.

The owner's ten exclusions are not imported: frame_0077, frame_0074, frame_0046, frame_0028, frame_0024, frame_0085, frame_0088, frame_0161, frame_0193 and frame_0206. No eligible original is missing. Run-prefixed card IDs and filenames, original identities and annotated-image checksums prevent duplicate entries.

Both files in each new pair are byte-for-byte copies of the source JPEGs at 1920 by 1440 pixels. They are not resized, re-encoded or reannotated. Exact frame IDs, source-video identity, dimensions, visual comparisons and pixel-content checks confirm pairing; EXIF metadata is absent in these source frames.

The visible saved YOLO labels identify ten alligator-cracking frames, two longitudinal-crack frames and four other-surface-defect frames. The existing category implementation supplies the additional Other surface defects group. Its layout, styles, JavaScript, independent BEFORE/AFTER buttons and full-size links are reused. Class IDs 0, 1 and 2 are tied to the rendered labels for this source; the separate density CSV's conflicting mapping is not used or changed. The expected model hash in run metadata is not presented as a verified checkpoint hash.

The photo verifier also accepts saved white annotation borders when they differ from the matching original, in addition to the existing blue/cyan borders. Source images, model files, detection sidecars, GPS and density/PDI records remain untouched. Detailed source paths, comparison sheets and preservation evidence remain in the private review directory.

## Run4 selections and caption cleanup - 26 October 2026

The owner subsequently selected run4 frames frame_0059, frame_0041, frame_0040, frame_0062, frame_0065 and frame_0163. All six have exact unannotated originals and were checked against their saved rendering, sidecars and source-video frame manifest.

Using a maximum 2 metre separation and great-circle distance between the saved frame GPS positions, run4 frame_0059 and frame_0163 each match their same-numbered run2 frame at 0 metres. Their complete BEFORE/AFTER gallery pairs replace the two older pairs. The four remaining run4 frames are added: their closest eligible run2 entries are 37.43 metres (frame_0041), 27.11 metres (frame_0040), 11.56 metres (frame_0062) and 45.47 metres (frame_0065) away. Run2 frame_0029 has no saved frame GPS and is retained without an inferred location.

The gallery now contains 38 entries: all 18 earlier curated entries, 14 run2 pairs and six run4 pairs. It has 36 BEFORE/AFTER pairs and the two original labelled-only examples. Superseded run2 gallery copies and records are archived privately; their RoadDefectResults sources remain unchanged. The ten original run2 exclusions remain excluded.

Per the owner's request, the repeated per-photo source and confidence-disclaimer paragraph is removed from every gallery card. Detection summaries, BEFORE/AFTER buttons, current-image links, filters and provenance data are retained. The existing category layout now includes a Potholes group for the selected saved pothole example. No unrelated website section is regenerated.

## Current Run2 photo batch - 26 October 2026

The Run2 directory was reused for a new photo-folder inference run processed at 09:59:26. It contains 39 annotated JPEGs, generated from the 51 unlabelled Run13 originals. This is distinct from the earlier Run2 video run, whose already-imported examples remain in the gallery. Batch-specific source metadata and identifiers preserve that distinction.

All 39 annotated photographs have matching original PNGs. The source PNGs and saved annotated JPEGs are copied byte-for-byte at their full 3840 by 2160 dimensions. The gallery checks now accept an unchanged PNG for BEFORE while retaining the annotated JPEG requirement for AFTER. No source file is resized, re-encoded or edited.

The owner explicitly selected updating the existing entry for 1788911598__PTS_000284. Its driving-longitudinal card ID and title are retained with the latest Run2 annotation and its exact original; the previous two display copies and prior record are archived privately. The other 38 pairs are added. This gives 76 gallery entries, comprising 74 matched pairs and the two existing labelled-only examples. All other 37 previous entries are retained unchanged.

Each pair was checked by exact identifier, equal dimensions, visual comparison, a luminance comparison at 640 by 360 pixels and visible annotation-border verification. The saved rendered labels were used to check this source's class mapping. Source PNG/JPEG hashes are recorded; the model hash expectation in run metadata is not presented as independently verified.

The existing category layout, controls, full-size links and default AFTER view are reused. The repeated per-photo provenance paragraph stays removed. Application code, model weights, run data, GPS and density/PDI information are not edited. Changes remain local without a commit, push or deployment.
