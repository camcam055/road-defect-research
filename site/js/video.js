/* One native player, three manually selectable stages. No third-party runtime. */
(() => {
  "use strict";
  const player = document.querySelector("#project-video-player");
  if (!player) return;
  const steps = Array.from(document.querySelectorAll("[data-video-stage]"));
  if (steps.length !== 3) return;
  const map = document.querySelector("#video-map");
  const status = document.querySelector("#video-status");
  const error = document.querySelector("#video-error");
  const frame = document.querySelector(".video-stage");
  const savedTimes = steps.map(() => 0);
  const completed = steps.map(() => false);
  let active = 0;
  let generation = 0;
  const formatTime = seconds => {
    const rounded = Math.round(seconds);
    return Math.floor(rounded / 60) + ":" + String(rounded % 60).padStart(2, "0");
  };
  const updateProgress = () => {
    const duration = player.duration;
    const progress = completed[active] ? 100 : Number.isFinite(duration) && duration > 0 ? Math.min(100, player.currentTime / duration * 100) : 0;
    steps[active].style.setProperty("--watch-progress", progress + "%");
  };
  const updateControls = () => {
    steps.forEach((step, index) => {
      const selected = index === active;
      if (selected) step.setAttribute("aria-current", "step");
      else step.removeAttribute("aria-current");
      step.classList.toggle("is-complete", completed[index]);
      const upNext = completed[active] && index === active + 1;
      step.classList.toggle("is-up-next", upNext);
      step.setAttribute("aria-label", "Video " + (index + 1) + " of 3: " + step.dataset.title + (completed[index] ? ", completed" : "") + (upNext ? ", up next" : ""));
      if (completed[index]) step.style.setProperty("--watch-progress", "100%");
    });
    const last = active === steps.length - 1;
    map.hidden = !last || !completed[active];
    map.classList.toggle("is-highlighted", last && completed[active]);
    if (completed[active]) {
      status.textContent = last ? "Road Defect Detection complete. Explore the results on the interactive map." : steps[active].dataset.title + " complete. Select " + steps[active + 1].dataset.title + " above to continue.";
    } else {
      status.textContent = "";
    }
  };
  const selectStage = (index, playRequested = false, force = false) => {
    if (index < 0 || index >= steps.length || index === active && !force) return;
    savedTimes[active] = Number.isFinite(player.currentTime) ? player.currentTime : 0;
    player.pause();
    active = index;
    const step = steps[active];
    const request = ++generation;
    error.hidden = true;
    document.querySelector("#video-current-stage").textContent = "STAGE " + String(active + 1).padStart(2, "0") + " / 03";
    document.querySelector("#video-title").textContent = step.dataset.title;
    document.querySelector("#video-description").textContent = step.dataset.description;
    document.querySelector("#video-duration-text").textContent = formatTime(Number(step.dataset.duration));
    player.setAttribute("aria-label", step.dataset.title + " — video " + (active + 1) + " of 3");
    player.poster = step.dataset.poster;
    player.src = step.dataset.src;
    player.load();
    updateControls();
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches && frame.animate) {
      frame.animate([{opacity: 0.35}, {opacity: 1}], {duration: 240, easing: "ease-out"});
    }
    if (playRequested) {
      const promise = player.play();
      if (promise) promise.catch(() => {
        if (generation === request && !player.error) status.textContent = "Press Play to continue with " + step.dataset.title + ".";
      });
    }
  };
  steps.forEach((step, index) => {
    step.addEventListener("click", () => selectStage(index, !player.paused || player.ended));
    step.addEventListener("keydown", event => {
      let target;
      if (event.key === "ArrowRight") target = (index + 1) % steps.length;
      if (event.key === "ArrowLeft") target = (index + steps.length - 1) % steps.length;
      if (event.key === "Home") target = 0;
      if (event.key === "End") target = steps.length - 1;
      if (target === undefined) return;
      event.preventDefault();
      selectStage(target, !player.paused || player.ended);
      steps[target].focus();
    });
  });
  document.querySelector("#video-retry").addEventListener("click", () => selectStage(active, true, true));
  player.addEventListener("loadedmetadata", () => {
    const saved = savedTimes[active];
    if (!completed[active] && saved > 0 && Number.isFinite(player.duration) && saved < player.duration) player.currentTime = saved;
    updateProgress();
  });
  player.addEventListener("timeupdate", updateProgress);
  player.addEventListener("contextmenu", event => event.preventDefault());
  player.addEventListener("ended", () => {
    completed[active] = true;
    savedTimes[active] = 0;
    updateProgress();
    updateControls();
  });
  player.addEventListener("error", () => {
    error.hidden = false;
    status.textContent = "This video could not be loaded. Try again or choose another stage.";
  });
  updateControls();
})();
