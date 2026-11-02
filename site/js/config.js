// Add the final MP4, then set videoSrc to "assets/video/project-demo.mp4".
window.SHOWCASE_CONFIG = { videoSrc: "", videoPoster: "" };

// Cloudflare Web Analytics: one official beacon shared by all website pages.
(() => {
  "use strict";
  if (document.querySelector('script[data-cf-beacon], script[src*="static.cloudflareinsights.com/beacon.min.js"]')) return;
  const beacon = document.createElement("script");
  beacon.type = "module";
  beacon.src = "https://static.cloudflareinsights.com/beacon.min.js";
  beacon.dataset.cfBeacon = '{"token":"8f0f3df76275416282ae9814f8cf52ab"}';
  document.head.appendChild(beacon);
})();
