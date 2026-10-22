(() => {
  const home = document.createElement("a");
  home.className = "research-home";
  home.href = "../../index.html";
  home.target = "_top";
  home.textContent = "Home";
  home.setAttribute("aria-label", "Return to all research sections");
  document.body.appendChild(home);
  const soil = [...document.body.children].find(el => el.style.position === "fixed" && el.textContent.includes("Soil class"));
  if (soil) {
    soil.classList.add("research-soil-legend");
    soil.id = "research-soil-legend";
    const button = document.createElement("button");
    button.className = "research-legend-button";
    button.type = "button";
    button.textContent = "Soil legend";
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("aria-controls", soil.id);
    button.addEventListener("click", () => {
      const open = soil.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(open));
    });
    document.body.appendChild(button);
  }
})();

(()=>{
const meta=document.querySelector('meta[name="viewport"]');
if(meta)meta.content="width=device-width,initial-scale=1";
document.querySelectorAll(".legend.leaflet-control svg").forEach(svg=>{
 const width=svg.getAttribute("width")||"450",height=svg.getAttribute("height")||"40";
 svg.setAttribute("viewBox","0 0 "+width+" "+height);
});
const layers=document.querySelector(".leaflet-control-layers");
if(layers){
 layers.classList.add("research-mobile-layers");
 const list=layers.querySelector(".leaflet-control-layers-list");
 if(!list)return;
 list.id="research-layer-list";
 const button=document.createElement("button");
 button.type="button";button.className="research-layers-button";button.textContent="Map layers";
 button.setAttribute("aria-expanded","false");button.setAttribute("aria-controls",list.id);
 button.addEventListener("click",()=>{
  const open=layers.classList.toggle("is-open");button.setAttribute("aria-expanded",String(open));
 });
 layers.prepend(button);
}
})();

// Report actual tile readiness; a loaded iframe alone does not prove a working basemap.
(() => {
  "use strict";
  const status = document.createElement("div");
  status.className = "research-basemap-status";
  status.setAttribute("role", "status");
  status.textContent = "Loading basemap…";
  document.body.appendChild(status);
  const mapElement = document.querySelector(".folium-map");
  if (mapElement) {
    mapElement.setAttribute("role", "region");
    mapElement.setAttribute("aria-label", "Road defect map. Use arrow keys to pan and plus or minus to zoom.");
  }
  const mapName = Object.keys(window).find(name => /^map_/.test(name) && window.L && window[name] instanceof L.Map);
  if (!mapName) {
    status.textContent = "The map could not start. Reload this page to try again.";
    document.documentElement.dataset.basemap = "error";
    return;
  }
  const map = window[mapName];
  const notify = state => {
    document.documentElement.dataset.basemap = state;
    if (window.parent !== window) window.parent.postMessage({type:"road-map-status", state}, window.location.protocol === "file:" ? "*" : window.location.origin);
  };
  let tileLayer;
  map.eachLayer(layer => { if (layer instanceof L.TileLayer) tileLayer = layer; });
  if (!tileLayer) { status.textContent = "No basemap is configured."; notify("error"); return; }
  let loaded = 0;
  const success = () => { loaded += 1; status.hidden = true; notify("loaded"); };
  const failure = () => {
    if (loaded) return;
    status.hidden = false;
    status.textContent = "Basemap tiles could not load. Check your internet connection. ";
    const retry = document.createElement("button");
    retry.type = "button"; retry.textContent = "Retry basemap";
    retry.addEventListener("click", () => { status.textContent = "Loading basemap…"; notify("loading"); tileLayer.redraw(); });
    status.appendChild(retry); notify("error");
  };
  tileLayer.on("tileload", success);
  tileLayer.on("tileerror", failure);
  const tiles = Object.values(tileLayer._tiles || {});
  if (tiles.some(tile => tile.el.complete && tile.el.naturalWidth > 0)) success();
  else {
    notify("loading");
    if (tiles.length && tiles.every(tile => tile.el.complete)) failure();
  }
  // Bound popup height and recalculate after lazy photos load so the close button stays visible.
  map.on("popupopen", event => {
    document.body.classList.add("research-popup-open");
    const popup = event.popup;
    popup.options.maxWidth = Math.max(180, Math.min(340, map.getSize().x - 70));
    popup.options.maxHeight = Math.max(80, Math.min(420, map.getSize().y - 130));
    popup.update();
    popup.getElement().querySelectorAll("img").forEach(img => {
      if (!img.complete) img.addEventListener("load", () => popup.update(), {once:true});
    });
  });
  map.on("popupclose", () => document.body.classList.remove("research-popup-open"));
  // Safari needs the Leaflet container recalculated after iframe and orientation changes.
  const resize = () => window.requestAnimationFrame(() => map.invalidateSize({pan:false}));
  window.addEventListener("resize", resize);
  window.addEventListener("orientationchange", resize);
  resize();
})();
