# Local website review — 27 October 2026

Status: local validation complete. The owner reviewed the website and explicitly approved commit, push and publication on 27 October 2026, retaining the existing URL. The checks below record the local review before publication.

Local preview: http://127.0.0.1:8766/

## Changes

- Homepage and research navigation now follow 01 The Problem, 02 Literature Review, 03 Methodology, 04 Results, 05 Conclusion and 06 Future Work.
- Conclusion uses 5.0; Future Work uses 6.0. Results discussion uses 4.5 to remove the former numbering gap. Their contents links and glossary source labels agree. Anchor IDs stay stable.
- Removed the entire Project Management material from Methodology: 14 report text blocks and four contents links, including progress/timeline, risks/mitigation and costs. No associated images or tables existed in those imported blocks. Its glossary pointer now targets the retained technical training passage.
- Removed Results Appendices D and F, their seven contents entries, seven text blocks, the one appendix-only pointer sentence, and eight exclusively used figure files. Main performance results, real-world testing, discussion and the Methodology model-parameter Appendix D remain.
- Removed the requested gallery count/provenance notice, gallery source-description line and glossary source-description line from both rendered pages and their generators.
- Replaced all three videos and corresponding posters with the newly supplied Data Collection, AI Training and Road Defect Detection files. Superseded website MP4/JPG copies and references are absent from the public folder; private recovery copies are retained.
- Updated source metadata, generators, validation, maintenance guidance and checksums. The shared design, CSS/JavaScript, map, gallery images and glossary definitions are preserved.

## Verification

- Project Management headings, content, source IDs and anchors are absent from all served HTML/JSON/JavaScript/CSS/CSV sources. No exclusive administrative assets remain. The Executive Summary remains excluded.
- All 304 retained report blocks and equations match the original report after the four existing privacy substitutions and three approved heading-number changes. Rebuilding in a separate private folder exactly reproduces the local research and shell HTML.
- Static validation passed: 13 HTML pages, 10 homepage cards and 1,679 local references; no broken local links or anchors.
- All three new videos pass full decoding, exact frame-count/dimension/timestamp checks, source/output hashes and fast-start checks. Source MOVs are unchanged. Poster and MP4 range requests match the local files.
- Browser checks passed for research order, contents anchors, removal of the Results appendices, gallery filters and BEFORE/AFTER controls, glossary search/clear/no-results/source links, video switching/playback and completion prompts.
- Desktop layouts checked at 1280 × 720 and 1280 × 900. Mobile layouts checked at 390 × 844 and 320 × 780 without horizontal page overflow. These are browser viewport checks; no physical phone was tested by the agent.
- The owner confirmed the new Data Collection video works.
- The original report, master map and source MOVs are unchanged. 2644 protected website files are byte-identical, including the interactive map, its assets, gallery images, shared CSS/JavaScript and publication workflow. All 76 gallery cards and 46 glossary definitions are unchanged.

## Files changed

The table includes maintenance records and the checksum manifest. Removed web assets have private recovery copies. The machine-readable list is LOCAL_FILE_CHANGES_20261027.json.

| Status | File |
|---|---|
| modified | MANIFEST.sha256 |
| modified | UPDATE_GUIDE.md |
| modified | docs/VIDEO_VERIFICATION.md |
| modified | site/content/conclusion.html |
| modified | site/content/future-work.html |
| modified | site/content/gallery.html |
| modified | site/content/glossary.html |
| modified | site/content/literature-review.html |
| modified | site/content/methodology.html |
| modified | site/content/problem.html |
| modified | site/content/references.html |
| modified | site/content/results.html |
| modified | site/data/glossary.json |
| modified | site/data/report-source.json |
| modified | site/data/videos.json |
| modified | site/index.html |
| modified | site/video.html |
| modified | tools/build_sections.py |
| modified | tools/check_site.py |
| modified | tools/extract_report.py |
| modified | tools/gallery_page.py |
| modified | tools/layout.py |
| modified | tools/video_checks.py |
| added | docs/LOCAL_FILE_CHANGES_20261027.json |
| added | docs/LOCAL_REVIEW_20261027.md |
| added | site/assets/video/ai-training-updated-20261027.jpg |
| added | site/assets/video/ai-training-updated-20261027.mp4 |
| added | site/assets/video/data-collection-updated-20261027.jpg |
| added | site/assets/video/data-collection-updated-20261027.mp4 |
| added | site/assets/video/road-defect-detection-updated-20261027.jpg |
| added | site/assets/video/road-defect-detection-updated-20261027.mp4 |
| removed | site/assets/figures/image16.jpeg |
| removed | site/assets/figures/image17.jpeg |
| removed | site/assets/figures/image18.jpeg |
| removed | site/assets/figures/image19.jpeg |
| removed | site/assets/figures/image29.png |
| removed | site/assets/figures/image30.png |
| removed | site/assets/figures/image31.png |
| removed | site/assets/figures/image32.png |
| removed | site/assets/video/ai-training-final-20261026.jpg |
| removed | site/assets/video/ai-training-final-20261026.mp4 |
| removed | site/assets/video/data-collection-trimmed-20261026.jpg |
| removed | site/assets/video/data-collection-trimmed-20261026.mp4 |
| removed | site/assets/video/road-to-results-final-20261026.jpg |
| removed | site/assets/video/road-to-results-final-20261026.mp4 |
