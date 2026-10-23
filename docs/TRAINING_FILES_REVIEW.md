# Training files and application reuse

Reviewed 23 October 2026. Scope: the organised training folder, the supplied Desktop website package, the existing GitHub checkout, and related saved application outputs.

## Useful assets incorporated

The website now uses 18 reviewed, already annotated photographs: 11 longitudinal-crack examples, five transverse-crack examples, and two alligator-cracking examples. Sixteen have confirmed matching originals; two remain labelled-only. The category directories and public manifest are reusable as a small visual smoke-test/reference set. They are not an independent model-evaluation dataset.

## Checkpoint identity

The organised Christchurch fine-tuning run's best checkpoint and the Train ai copy of best_chch_driving.pt have the same SHA-256 as the current upgraded application's configured checkpoint:

523b481069c4dbd70922801c5e54750619befe566f352cd1654a3944bade7d46

This is an existing capability, rather than evidence of a new model upgrade. Other large/extra-large and temporary-run checkpoints are different artifacts; the available training logs do not establish that switching to one would improve unseen-road performance. The application checkpoint and detection settings were preserved.

## Class IDs require an explicit mapping

The historical application output and current model use different numeric orders. This was checked against the application code, configuration, saved sidecars and visible labels.

| ID | Historical application output | Current checkpoint |
| --- | --- | --- |
| 0 | Alligator crack | Pothole |
| 1 | Longitudinal crack | Longitudinal crack |
| 2 | Other corruption | Transverse crack |
| 3 | Pothole | Alligator crack |
| 4 | Transverse crack | Other corruption |

A reusable importer must carry the source class manifest and remap IDs by class name. Applying today's class order to old labels would silently corrupt the classifications. The gallery records mappings per source. It does not relabel old boxes as predictions from the current checkpoint.

## Data useful for subsequent application work

- Matched Dataset supplies 51 image/label pairs; the New Zealand photos and labels provide further local examples. Class-name provenance must be established before any training import because the supplied exports do not include a complete class-name manifest.
- Saved annotated outputs can support manual regression inspection. Some predictions visibly box leaves, vehicles or non-defect features, so they cannot be adopted wholesale as ground truth.
- The training configuration and results files document earlier model runs. Small or incomplete local exports are not evidence of independent generalisation, and the Train ai download is a numbered archive part.
- Some text files contain six-value prediction rows with confidence, while training labels normally contain five values. These are different record types; preserve that distinction and handle empty labels deliberately.

Original datasets, checkpoints, report evidence and application code remain outside this website change. Raw model weights and private source mappings are excluded from the repository and deployment.
