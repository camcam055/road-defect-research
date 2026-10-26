# Project video verification — 26 October 2026

The Project Video page uses only the final sources supplied by the owner, in this order:

1. `Data Collection Video new.mov` → Data Collection
2. `Training the AI new.mov` → AI Training
3. `From Road to Results.mov` → Road Defect Detection

`site/data/videos.json` records the source names and SHA-256 checksums, output checksums, dimensions, durations and byte counts. All three original source files still match their recorded hashes. The source MOV files remain outside the website; no original was renamed or modified.

The published copies are silent H.264/yuv420p MP4s with fast-start metadata, at the original dimensions (1440×1080, 1920×910 and 1720×1080). The silent audio tracks were removed at the owner's request without re-encoding the converted video. Each MP4 is under 100 MiB. The three final MP4s passed full video decoding without errors.

## Observed local checks

- The static site checker passes: 13 HTML pages, 10 homepage cards, 8,577 local references and no errors. The deployable directory is 796,107,560 bytes.
- Browser checks at 1280×900, 390×844 and 320×780 showed no horizontal page overflow. The first video loads paused; exactly one native player is present.
- All three stage buttons select the correct final source, title, description and poster. Home and ArrowRight keyboard navigation moved both selection and focus correctly.
- The first video completed through playback. Native keyboard seeking also exercised the AI Training and detection completion events. Completed stages receive check marks; the next stage receives the completion highlight. Clicking a stage after completion starts that selected video.
- Finishing the final video reveals `Explore Interactive Map →` with `href="map.html"`. The existing local interactive map loads with its Back link, clusters and basemap.
- The lower Previous/Next buttons, direct video links and visible playback guidance were removed as requested. The native download option is suppressed with `controlslist="nodownload"`; the player menu starts with Playback speed. Native sound controls are hidden and the final media has no audio stream. The player's context menu is suppressed.
- JavaScript and Python syntax checks pass. The maintained video renderer reproduces the saved page, so a future normal site rebuild retains this experience.
- The local preview server supports video byte ranges. Full-page GET, MP4 MIME type, start/middle/suffix/open-ended ranges, HEAD and invalid-range responses passed. Native seeking works with the complete video duration available.
- A repository-wide before/after SHA-256 comparison confirms that existing files outside the named video/supporting documentation/preview changes remain byte-identical. In particular, the current homepage, research pages, gallery, glossary and map files were preserved.

## Boundaries

These are local desktop browser checks, including phone-size viewports; no physical phone or live GitHub Pages deployment was tested. Relative asset URLs, browser-compatible encoding, fast-start metadata, asset checksums and GitHub file-size limits were checked locally.

Hiding download controls and removing direct links changes the interface; it is not copy protection. A determined visitor can still save or capture browser-playable media.

No Git commit, push, publication or deployment was performed. The owner's local preview remains at `http://127.0.0.1:8778/video.html`.
