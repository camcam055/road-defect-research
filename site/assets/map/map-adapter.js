(() => {
  "use strict";
  const home = document.createElement("a");
  home.className = "research-home";
  home.href = "../../index.html";
  home.target = "_top";
  home.textContent = "Home";
  home.setAttribute("aria-label", "Return to all research sections");
  document.body.appendChild(home);
  const element = document.querySelector(".folium-map");
  if (element) {
    element.setAttribute("role", "region");
    element.setAttribute("aria-label", "Road defect map. Use arrow keys to pan and plus or minus to zoom.");
  }
  const sourceStatus = document.getElementById("basemap-status");
  const mapName = Object.keys(window).find(name => /^map_/.test(name) && window.L && window[name] instanceof L.Map);
  const relay = () => {
    const state = !mapName ? "error" : sourceStatus && sourceStatus.textContent.startsWith("Connecting") ? "loading" : "loaded";
    document.documentElement.dataset.basemap = state;
    if (window.parent !== window) {
      window.parent.postMessage({type: "road-map-status", state}, window.location.protocol === "file:" ? "*" : window.location.origin);
    }
  };
  if (sourceStatus) {
    sourceStatus.setAttribute("role", "status");
    new MutationObserver(relay).observe(sourceStatus, {childList: true, characterData: true, subtree: true});
  }
  if (mapName) {
    const map = window[mapName];
    map.on("popupopen", () => document.documentElement.classList.add("research-popup-open"));
    map.on("popupclose", () => document.documentElement.classList.remove("research-popup-open"));
  }
  relay();
})();
