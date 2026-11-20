/* Version 2 only: a thin reading progress line at the top of the page. */
(function () {
  var bar = document.createElement("div");
  bar.className = "progress";
  bar.setAttribute("aria-hidden", "true");
  document.body.appendChild(bar);
  var ticking = false;
  var paint = function () {
    ticking = false;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, window.scrollY / max) : 0) + ")";
  };
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(paint); }
  }, { passive: true });
  paint();
})();
