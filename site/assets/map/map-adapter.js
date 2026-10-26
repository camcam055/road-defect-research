(() => {
  "use strict";
  if (window.parent === window) {
    const back = document.createElement("a");
    back.className = "research-home";
    back.href = "../../index.html";
    back.textContent = "← Back";
    back.setAttribute("aria-label", "Back to all research sections");
    document.body.appendChild(back);
  }
  const element = document.querySelector(".folium-map");
  if (element) {
    element.setAttribute("role", "region");
    element.setAttribute("aria-label", "Road defect map. Use arrow keys to pan and plus or minus to zoom.");
  }
  const mapName = Object.keys(window).find(name => /^map_/.test(name) && window.L && window[name] instanceof L.Map);
  if (mapName) {
    const map = window[mapName];
    // Present every saved run under one owner-requested defect switch.
    // Keep the original groups, clusters, coordinates and popup metadata intact.
    const layersName = Object.keys(window).find(name => /^layer_control_.*_layers$/.test(name) && window[name].overlays);
    const definition = window.RESEARCH_MAP_CONTEXT ? window.RESEARCH_MAP_CONTEXT.layers : layersName && window[layersName];
    const control = window.RESEARCH_MAP_CONTEXT ? window.RESEARCH_MAP_CONTEXT.control : layersName && window[layersName.replace(/_layers$/, "")];
    if (definition && control) {
      const defects = Object.entries(definition.overlays).filter(([label]) => /^Road defects(?:\s|$)/.test(label));
      if (defects.length > 1) {
        const allDefects = L.featureGroup();
        defects.forEach(([label, layer]) => {
          control.removeLayer(layer);
          if (map.hasLayer(layer)) map.removeLayer(layer);
          allDefects.addLayer(layer);
          delete definition.overlays[label];
        });
        allDefects.addTo(map);
        control.addOverlay(allDefects, "Road defects");
        definition.overlays["Road defects"] = allDefects;
      }
    }
    const setPopupState = open => {
      document.documentElement.classList.toggle("research-popup-open", open);
      if (window.parent !== window) {
        try { window.parent.document.documentElement.classList.toggle("research-popup-open", open); }
        catch (_) { /* Standalone map remains fully usable in an external embed. */ }
      }
    };
    map.on("popupopen", () => setPopupState(true));
    map.on("popupclose", () => setPopupState(false));
  }
})();
