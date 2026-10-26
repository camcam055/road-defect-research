# Project videos — local verification, 27 October 2026

All three owner-supplied replacement videos passed local review. The owner explicitly approved publication on 27 October 2026, keeping the existing website URL.

| Stage | Source | Source duration | Dimensions | Frames retained | Website MP4 |
|---|---|---:|---|---:|---|
| 01 Data Collection | Updated data collection 01.mov | 50.923 s | 960 × 720 | 3053 | assets/video/data-collection-updated-20261027.mp4 |
| 02 AI Training | 02 AI training.mov | 92.546 s | 1280 × 606 | 5237 | assets/video/ai-training-updated-20261027.mp4 |
| 03 Road Defect Detection | 03 Road defect detection.mov | 76.806 s | 1146 × 720 | 2712 | assets/video/road-defect-detection-updated-20261027.mp4 |

Each web copy is silent H.264/yuv420p with fast-start metadata, preserving the existing silent-player convention. No extra cuts or speed changes were applied. All source frames are retained and every frame presentation timestamp matches the supplied source exactly. The final frame's MP4 duration can differ slightly from its MOV container duration; frame content and presentation timestamps match.

All MP4s passed complete decoding, frame-count/dimension checks, monotonic decode timestamp checks, recorded SHA-256/size checks and the existing video-site validator. Each remains below 100 MiB. Posters are taken from their corresponding replacement video. Earlier website MP4/JPG copies are absent from the public folder and have private recovery copies. Original MOVs are unchanged outside the repository.

## Browser checks

- All three stages load the correct new MP4 and poster and play without media errors.
- The new Data Collection video reaches its end at 50.923 seconds and highlights AI Training as the next stage. The owner also confirmed that it works.
- The Road Defect Detection video completes and reveals the existing Explore Interactive Map link.
- Stage switching, native controls and keyboard activation remain available. Browser-compatible MP4 byte-range requests return 206 with matching bytes.
- Desktop video layout checked at 1280 × 900; phone layouts checked at 390 × 844 and 320 × 780 without horizontal page overflow.
- The one-player layout, styling and JavaScript are unchanged. Physical-device playback was not tested by the agent.

These checks were completed before publication. The owner has since explicitly approved committing, pushing and publishing the reviewed update.
