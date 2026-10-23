(() => {
  "use strict";
  const toc = document.querySelector(".toc");
  if (toc && window.matchMedia("(min-width: 761px)").matches) toc.open = true;
  const video = document.querySelector("#project-video");
  if (video) {
    const config = window.SHOWCASE_CONFIG || {};
    if (config.videoSrc) {
      video.src = config.videoSrc;
      if (config.videoPoster) video.poster = config.videoPoster;
      const placeholder = document.querySelector("#video-placeholder");
      video.addEventListener("loadedmetadata", () => { video.hidden = false; placeholder.hidden = true; });
      const download = document.querySelector("#video-download");
      download.href = config.videoSrc;
      download.hidden = false;
      video.addEventListener("error", () => {
        video.hidden = true;
        placeholder.hidden = false;
        document.querySelector("#video-error").hidden = false;
      });
    }
  }
  const map = document.querySelector("#defect-map");
  if (map) {
    window.addEventListener("message", event => {
      if (event.source !== map.contentWindow || event.origin !== window.location.origin || !event.data || event.data.type !== "road-map-status") return;
      const loading = document.querySelector("#map-loading");
      loading.hidden = event.data.state === "loaded" || event.data.state === "error";
      if (event.data.state === "loading") loading.textContent = "Loading the basemap…";
    });
    window.setTimeout(() => {
      const loading = document.querySelector("#map-loading");
      if (!loading.hidden) loading.textContent = "The map is still loading. You can also use Open map.";
    }, 15000);
  }
})();

// Section 07: switch only the selected photograph, preserving scroll position.
(() => {
  "use strict";
  document.querySelectorAll("[data-gallery]").forEach(card => {
    card.querySelectorAll("[data-view]").forEach(button => {
      button.addEventListener("click", () => {
        const view = button.dataset.view;
        card.querySelectorAll("[data-view]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
        card.querySelectorAll("[data-image]").forEach(item => { item.hidden = item.dataset.image !== view; });
        const selected = card.querySelector('[data-image="' + view + '"]');
        card.querySelector(".gallery-full").href = selected.getAttribute("src");
        card.querySelector(".gallery-state").textContent = view === "before" ? "Before · Original photograph" : "After · Saved labelled photograph";
      });
    });
  });
  const categoryGroups = Array.from(document.querySelectorAll("[data-gallery-category]"));
  const filterButtons = Array.from(document.querySelectorAll("[data-gallery-filter]"));
  filterButtons.forEach(button => {
    button.addEventListener("click", () => {
      const category = button.dataset.galleryFilter;
      filterButtons.forEach(item => item.setAttribute("aria-pressed", String(item === button)));
      let count = 0;
      categoryGroups.forEach(group => {
        const match = category === "all" || group.dataset.galleryCategory === category;
        group.hidden = !match;
        if (match) count += group.querySelectorAll("[data-gallery]").length;
      });
      document.querySelector("#gallery-count").textContent = count + (count === 1 ? " photo" : " photos");
    });
  });
  const search = document.querySelector("#glossary-search");
  if (!search) return;
  const entries = Array.from(document.querySelectorAll(".glossary-entry"));
  const normalise = value => value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[-_]/g, " ");
  const indexed = entries.map(element => ({element, text: normalise(element.dataset.search)}));
  const update = () => {
    const words = normalise(search.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    indexed.forEach(item => {
      const match = words.every(word => item.text.includes(word));
      item.element.hidden = !match;
      if (match) count += 1;
    });
    document.querySelector("#glossary-count").textContent = count + (count === 1 ? " term" : " terms") + (words.length ? " found" : "");
    document.querySelector("#glossary-empty").hidden = count !== 0;
  };
  search.addEventListener("input", update);
  search.addEventListener("search", update);
  document.querySelector("#glossary-clear").addEventListener("click", () => { search.value = ""; update(); search.focus(); });
  update();
})();
