(function () {
  var root = document.documentElement;
  /* a version can switch all motion off with <html data-motion="off"> */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches || root.getAttribute("data-motion") === "off";

  /* mobile menu */
  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav-toggle");
  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open);
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      document.body.style.overflow = open ? "hidden" : "";
    });
  }

  /* light / dark theme toggle */
  var themeBtn = document.querySelector(".theme-toggle");
  if (themeBtn) {
    var syncThemeBtn = function () {
      var dark = root.getAttribute("data-theme") === "dark";
      themeBtn.setAttribute("aria-pressed", dark);
      themeBtn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
    };
    themeBtn.addEventListener("click", function () {
      var dark = root.getAttribute("data-theme") === "dark";
      if (dark) { root.removeAttribute("data-theme"); } else { root.setAttribute("data-theme", "dark"); }
      try { localStorage.setItem("theme-mode-v1", dark ? "light" : "dark"); } catch (e) { }
      syncThemeBtn();
    });
    syncThemeBtn();
  }

  /* section reveals, once each */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* silent looping clips play only while visible; with reduced motion they get controls instead */
  var vids = document.querySelectorAll("video[data-autoplay]");
  if (reduce) {
    vids.forEach(function (v) { if (!v.closest(".intro-bg")) v.controls = true; }); /* a background video just shows its still picture */
  } else if (vids.length && "IntersectionObserver" in window) {
    var vo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.play().catch(function () {}); } else { e.target.pause(); }
      });
    }, { threshold: 0.25 });
    vids.forEach(function (v) { vo.observe(v); });
  }

  /* carousel: arrows, keyboard, swipe, and an automatic change every 8 seconds.
     The active slide's video plays only while the carousel is on screen. */
  var AUTO_MS = 8000; /* time on each slide; 0 switches the automatic change off */
  document.querySelectorAll(".carousel").forEach(function (car) {
    var slides = car.querySelectorAll(".slide");
    var caption = car.querySelector(".carousel-caption");
    var count = car.querySelector(".carousel-count");
    var i = 0;
    var onScreen = false;
    var hold = false; /* true while the pointer or the keyboard focus is on the carousel */
    var timer = null;
    var sync = function () {
      slides.forEach(function (s, k) {
        var v = s.querySelector("video");
        if (!v) { return; }
        if (reduce) { v.controls = true; return; }
        if (k === i && onScreen) { v.play().catch(function () {}); } else { v.pause(); }
      });
    };
    var arm = function () {
      window.clearTimeout(timer);
      if (reduce || !AUTO_MS || !onScreen || hold || document.hidden) { return; }
      timer = window.setTimeout(function () { show(i + 1); }, AUTO_MS);
    };
    var show = function (n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle("is-active", k === i); });
      caption.textContent = slides[i].querySelector("figcaption").textContent;
      count.textContent = (i + 1) + " / " + slides.length;
      sync();
      arm(); /* a manual change restarts the 8 seconds */
    };
    car.querySelectorAll("[data-step]").forEach(function (b) {
      b.addEventListener("click", function () { show(i + Number(b.dataset.step)); });
    });
    car.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { show(i - 1); }
      if (e.key === "ArrowRight") { show(i + 1); }
    });
    var x0 = null;
    car.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    car.addEventListener("touchend", function (e) {
      if (x0 === null) { return; }
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) { show(i + (dx < 0 ? 1 : -1)); }
      x0 = null;
    });
    var setHold = function (h) { hold = h; arm(); };
    car.addEventListener("mouseenter", function () { setHold(true); });
    car.addEventListener("mouseleave", function () { setHold(false); });
    car.addEventListener("focusin", function () { setHold(true); });
    car.addEventListener("focusout", function () { setHold(false); });
    document.addEventListener("visibilitychange", arm);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        onScreen = entries[0].isIntersecting;
        sync();
        arm();
      }, { threshold: 0.2 }).observe(car);
    } else {
      onScreen = true;
    }
    show(0);
  });

  /* media pages: a gallery too long for a single grid is split into a few pages of a few
     pictures each, one page shown at a time, switching to the next on its own every 9 seconds
     (unless data-auto="false", e.g. a simple two-video toggle switched only by its button) */
  var PAGE_MS = 9000;
  document.querySelectorAll(".media-pages").forEach(function (wrap) {
    var pages = wrap.querySelectorAll(".media-page");
    if (pages.length < 2) { return; }
    var auto = wrap.getAttribute("data-auto") !== "false";
    var ms = parseInt(wrap.getAttribute("data-interval"), 10) || PAGE_MS;
    var dots = wrap.parentNode.querySelectorAll(".media-dots button");
    var nextBtn = wrap.parentNode.querySelector("[data-page-next]");
    var i = 0, onScreen = false, timer = null;
    var sync = function () {
      pages.forEach(function (p, k) {
        var v = p.querySelector("video");
        if (!v) { return; }
        if (reduce) { v.controls = true; return; }
        if (k === i && onScreen) { v.play().catch(function () {}); } else { v.pause(); }
      });
    };
    var arm = function () {
      window.clearTimeout(timer);
      if (!auto || reduce || !onScreen || document.hidden) { return; }
      timer = window.setTimeout(function () { show(i + 1); }, ms);
    };
    var show = function (n) {
      i = (n + pages.length) % pages.length;
      pages.forEach(function (p, k) { p.classList.toggle("is-active", k === i); });
      dots.forEach(function (d, k) { d.classList.toggle("is-active", k === i); d.setAttribute("aria-pressed", k === i); });
      if (nextBtn) {
        nextBtn.setAttribute("aria-label", i === 0 ? nextBtn.getAttribute("data-label-next") : nextBtn.getAttribute("data-label-prev"));
        nextBtn.textContent = i === 0 ? nextBtn.getAttribute("data-text-next") : nextBtn.getAttribute("data-text-prev");
      }
      sync();
      arm();
    };
    dots.forEach(function (d, k) { d.addEventListener("click", function () { show(k); }); });
    if (nextBtn) { nextBtn.addEventListener("click", function () { show(i + 1); }); }
    document.addEventListener("visibilitychange", arm);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        onScreen = entries[0].isIntersecting;
        sync();
        arm();
      }, { threshold: 0.2 }).observe(wrap);
    } else {
      onScreen = true;
    }
    show(0);
  });

  /* click to play: each panel toggles its own animation, one button drives them all */
  document.querySelectorAll("[data-play-group]").forEach(function (group) {
    var panels = group.querySelectorAll(".case-video");
    var all = group.parentNode.querySelector(".cases-all");
    var set = function (btn, play) {
      var v = btn.querySelector("video");
      if (play) { v.play().catch(function () {}); } else { v.pause(); }
      btn.classList.toggle("is-playing", play);
    };
    var refresh = function () {
      if (!all) { return; }
      var any = group.querySelector(".case-video.is-playing");
      all.querySelector("span").textContent = any ? "Pause all" : "Play all";
      all.querySelector("i").className = any ? "ph ph-pause" : "ph ph-play";
    };
    panels.forEach(function (btn) {
      btn.addEventListener("click", function () { set(btn, !btn.classList.contains("is-playing")); refresh(); });
    });
    if (all) {
      all.addEventListener("click", function () {
        var play = !group.querySelector(".case-video.is-playing");
        panels.forEach(function (btn) {
          if (play) { btn.querySelector("video").currentTime = 0; }
          set(btn, play);
        });
        refresh();
      });
    }
  });

  /* research interests as a map: items placed around the centre, links drawn in an SVG behind them */
  document.querySelectorAll(".interests-map").forEach(function (map) {
    var hub = map.querySelector(".eyebrow");
    var items = Array.prototype.slice.call(map.querySelectorAll(".chips li"));
    if (!hub || items.length < 3) { return; }
    var NS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "map-lines");
    svg.setAttribute("aria-hidden", "true");
    map.insertBefore(svg, map.firstChild);
    map.classList.add("is-map");
    var lines = [];
    var link = function (a, b, cls, nodes) {
      var l = document.createElementNS(NS, "line");
      l.setAttribute("x1", a.x); l.setAttribute("y1", a.y);
      l.setAttribute("x2", b.x); l.setAttribute("y2", b.y);
      l.setAttribute("pathLength", "1");
      l.setAttribute("class", cls);
      svg.appendChild(l);
      lines.push({ el: l, nodes: nodes });
    };
    var layout = function () {
      var W = map.clientWidth, n = items.length;
      var column = W < 420;
      map.classList.toggle("is-column", column);
      map.classList.toggle("is-compact", !column && W < 520);
      var H = map.clientHeight, c, pts;
      if (column) {
        /* narrow: centre on the left, interests stacked on the right */
        var x0 = 88 + 36, step = H / n;
        c = { x: 44, y: H / 2 };
        pts = items.map(function (li, k) { return { x: x0 + li.offsetWidth / 2, y: step * (k + 0.5), ax: x0 + 20 }; });
      } else {
        var w = 0, h = 0;
        items.forEach(function (li) { w = Math.max(w, li.offsetWidth); h = Math.max(h, li.offsetHeight); });
        var rx = W / 2 - w / 2 - 2, ry = H / 2 - h / 2 - 2;
        c = { x: W / 2, y: H / 2 };
        pts = items.map(function (li, k) {
          var a = -Math.PI / 2 + k * 2 * Math.PI / n;
          return { x: c.x + rx * Math.cos(a), y: c.y + ry * Math.sin(a) };
        });
      }
      hub.style.setProperty("--x", c.x + "px");
      hub.style.setProperty("--y", c.y + "px");
      svg.textContent = "";
      lines = [];
      items.forEach(function (li, k) {
        li.style.setProperty("--x", pts[k].x + "px");
        li.style.setProperty("--y", pts[k].y + "px");
        li.style.setProperty("--i", k);
        link(c, column ? { x: pts[k].ax, y: pts[k].y } : pts[k], "spoke", [k]);
      });
    };
    items.forEach(function (li, k) {
      var mark = function (on) {
        lines.forEach(function (l) { l.el.classList.toggle("on", on && l.nodes.indexOf(k) > -1); });
      };
      li.addEventListener("mouseenter", function () { mark(true); });
      li.addEventListener("mouseleave", function () { mark(false); });
    });
    layout();
    if ("ResizeObserver" in window) { new ResizeObserver(layout).observe(map); }
    window.addEventListener("resize", layout);
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(layout); }
    if (reduce || !("IntersectionObserver" in window)) {
      map.classList.add("drawn");
    } else {
      var mo = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) { map.classList.add("drawn"); mo.disconnect(); }
      }, { threshold: 0.3 });
      mo.observe(map);
    }
  });

  /* ---------- header designs of the inner pages (see "header designs" in css/site.css) ---------- */

  /* design 5, film strip: repeat the pictures so the strip can loop without a gap */
  document.querySelectorAll(".head-media").forEach(function (m) {
    var imgs = Array.prototype.slice.call(m.querySelectorAll("img"));
    if (!imgs.length) { return; }
    m.style.setProperty("--n", imgs.length);
    var copies = Math.ceil(2600 / (imgs.length * 316));
    for (var c = 0; c < copies; c++) {
      imgs.forEach(function (img) { m.appendChild(img.cloneNode(true)); });
    }
  });

  /* design 4, robot drawing: one small scene per page, drawn on a canvas in the colours of the theme.
     research: an arm brings a cable to a target shape; projects: two arms drape a sheet on a mold;
     outreach: an arm stacks and unstacks blocks. */
  document.querySelectorAll("canvas.head-anim").forEach(function (cv) {
    var ctx = cv.getContext && cv.getContext("2d");
    if (!ctx) { return; }
    var W = 460, H = 330, FLOOR = 318;
    var scene = cv.getAttribute("data-scene");
    var col = {};
    var readColours = function () {
      var cs = window.getComputedStyle(root);
      ["text", "muted", "line", "accent", "surface", "surface-2"].forEach(function (k) {
        col[k] = cs.getPropertyValue("--" + k).trim() || "#888";
      });
    };
    var ease = function (u) { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };
    var mix = function (a, b, u) { return a + (b - a) * u; };
    var path = function (pts, width, colour, dash) {
      ctx.beginPath();
      pts.forEach(function (p, k) { if (k) { ctx.lineTo(p[0], p[1]); } else { ctx.moveTo(p[0], p[1]); } });
      ctx.lineWidth = width; ctx.strokeStyle = colour; ctx.lineCap = "round"; ctx.lineJoin = "round";
      ctx.setLineDash(dash || []); ctx.stroke(); ctx.setLineDash([]);
    };
    var dot = function (x, y, r, colour) { ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832); ctx.fillStyle = colour; ctx.fill(); };
    var table = function () { path([[24, FLOOR], [W - 24, FLOOR]], 2, col.line); };
    /* a two-link arm on a pedestal, reaching the point (tx, ty); "left" bends the elbow for a target on the left */
    var arm = function (bx, by, tx, ty, left) {
      var l1 = 118, l2 = 104;
      var dx = tx - bx, dy = ty - by;
      var d = Math.max(l1 - l2 + 2, Math.min(Math.sqrt(dx * dx + dy * dy), l1 + l2 - 2));
      var a = Math.atan2(dy, dx);
      var k = Math.acos((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)) * (left ? 1 : -1);
      var ex = bx + l1 * Math.cos(a + k), ey = by + l1 * Math.sin(a + k);
      var px = bx + d * Math.cos(a), py = by + d * Math.sin(a);
      ctx.fillStyle = col.text;
      ctx.fillRect(bx - 18, by, 36, FLOOR - by);
      ctx.fillRect(bx - 30, FLOOR - 8, 60, 8);
      [[bx, by, ex, ey], [ex, ey, px, py]].forEach(function (s) {
        path([[s[0], s[1]], [s[2], s[3]]], 18, col.text);
        path([[s[0], s[1]], [s[2], s[3]]], 12, col.surface);
      });
      dot(bx, by, 12, col.text); dot(bx, by, 4, col.accent);
      dot(ex, ey, 10, col.text); dot(ex, ey, 3.5, col.accent);
      dot(px, py, 7, col.text); dot(px, py, 3, col.surface);
    };

    /* research: cable from a fixture on the table to the gripper, modeled as a circular arc of fixed
       length (solved in closed form from the two endpoints) so its total length never changes, only
       its bend does: a tighter reach leaves more slack, so it bows more; a fuller reach straightens it. */
    var poses = [[215, 150], [258, 222], [178, 205]];
    var CABLE_N = 32, CABLE_LEN = 230;
    var cable = function (g) {
      var f = [78, FLOOR - 10], pts = [], k;
      var dx = g[0] - f[0], dy = g[1] - f[1], d = Math.min(Math.sqrt(dx * dx + dy * dy) || 1, CABLE_LEN * 0.999);
      var tx = dx / d, ty = dy / d, nx = ty, ny = -tx; /* perpendicular, bows up and to the left */
      var lo = 1e-6, hi = Math.PI - 1e-6, ratio = CABLE_LEN / d, theta = 0;
      for (var it = 0; it < 40; it++) {
        theta = (lo + hi) / 2;
        if (theta / Math.sin(theta) < ratio) { lo = theta; } else { hi = theta; }
      }
      var R = d / (2 * Math.sin(theta)), cosT = Math.cos(theta);
      var mx = f[0] + tx * d / 2, my = f[1] + ty * d / 2;
      var cx = mx - nx * R * cosT, cy = my - ny * R * cosT;
      for (k = 0; k <= CABLE_N; k++) {
        var phi = -theta + 2 * theta * (k / CABLE_N), cp = Math.cos(phi), sp = Math.sin(phi);
        pts.push([cx + R * (cp * nx + sp * tx), cy + R * (cp * ny + sp * ty)]);
      }
      return pts;
    };
    var research = function (t) {
      var T = 5, n = Math.floor(t / T) % poses.length, u = (t % T) / T;
      var from = poses[n], to = poses[(n + 1) % poses.length], e = ease(u / 0.6);
      var g = [mix(from[0], to[0], e), mix(from[1], to[1], e)];
      var pts = cable(g), done = u >= 0.6;
      table();
      ctx.fillStyle = col.text; ctx.fillRect(64, FLOOR - 16, 28, 16);
      path(cable(to), 2, col.accent, [6, 7]);
      arm(376, 232, g[0], g[1], true);
      path(pts, 6, done ? col.accent : col.text);
      /* small frames along the cable, as in the shape servoing figures */
      [6, 13, 20, 27].forEach(function (k) {
        var p = pts[k], q = pts[k + 1], len = Math.sqrt(Math.pow(q[0] - p[0], 2) + Math.pow(q[1] - p[1], 2)) || 1;
        var tx = (q[0] - p[0]) / len, ty = (q[1] - p[1]) / len;
        path([p, [p[0] + ty * 14, p[1] - tx * 14]], 2, col.muted);
        dot(p[0], p[1], 3.5, col.surface); dot(p[0], p[1], 2, col.text);
      });
      dot(g[0], g[1], 7, col.text); dot(g[0], g[1], 3, col.surface);
    };

    /* projects: two arms lower a sheet, which settles on the mold */
    var moldY = function (x) {
      var u = (x - 160) / 140;
      return FLOOR - 2 - (u > 0 && u < 1 ? 58 * (0.5 - 0.5 * Math.cos(6.2832 * u)) : 0);
    };
    var projects = function (t) {
      var T = 8, u = (t % T) / T;
      var s = u < 0.4 ? ease(u / 0.4) : u < 0.62 ? 1 : u < 0.9 ? 1 - ease((u - 0.62) / 0.28) : 0;
      var xl = mix(152, 134, s), xr = mix(308, 326, s), yg = mix(176, FLOOR - 8, s);
      var mold = [], sheet = [], k;
      for (k = 0; k <= 40; k++) { mold.push([160 + 3.5 * k, moldY(160 + 3.5 * k)]); }
      for (k = 0; k <= 40; k++) {
        var x = mix(xl, xr, k / 40);
        sheet.push([x, Math.min(yg + 24 * Math.sin(3.1416 * k / 40), moldY(x) - 3)]);
      }
      table();
      ctx.beginPath();
      mold.forEach(function (p, i) { if (i) { ctx.lineTo(p[0], p[1]); } else { ctx.moveTo(p[0], p[1]); } });
      ctx.closePath(); ctx.fillStyle = col["surface-2"]; ctx.fill();
      path(mold, 2, col.text);
      arm(58, 232, xl, yg, false);
      arm(402, 232, xr, yg, true);
      path(sheet, 5, col.accent);
    };

    /* outreach: pick the blocks one by one, stack them, then put them back */
    var src = [[176, FLOOR - 28], [210, FLOOR - 28], [244, FLOOR - 28]], stackX = 304, hover = 196, steps = [];
    var go = function (x, y, dur, act, k) { steps.push({ x: x, y: y, dur: dur, act: act, k: k }); };
    var carry = function (k, ax, ay, bx, by) {
      go(ax, hover, 0.6); go(ax, ay, 0.4, "grab", k); go(ax, hover, 0.4);
      go(bx, hover, 0.6); go(bx, by, 0.4, "drop", k); go(bx, hover, 0.4);
    };
    [2, 1, 0].forEach(function (k, n) { carry(k, src[k][0], src[k][1], stackX, FLOOR - 28 - 28 * n); });
    go(stackX, hover, 1.2);
    [0, 1, 2].forEach(function (k, n) { carry(k, stackX, FLOOR - 28 - 28 * (2 - n), src[k][0], src[k][1]); });
    go(src[2][0], hover, 1.2);
    var total = steps.reduce(function (s, st) { return s + st.dur; }, 0);
    var outreach = function (t) {
      var tt = t % total, pos = [src[2][0], hover], held = -1;
      var blocks = src.map(function (p) { return [p[0], p[1]]; });
      for (var i = 0; i < steps.length; i++) {
        var st = steps[i];
        if (tt >= st.dur) {
          tt -= st.dur; pos = [st.x, st.y];
          if (st.act === "grab") { held = st.k; }
          if (st.act === "drop") { blocks[st.k] = [st.x, st.y]; held = -1; }
        } else {
          var e = ease(tt / st.dur);
          pos = [mix(pos[0], st.x, e), mix(pos[1], st.y, e)];
          break;
        }
      }
      if (held > -1) { blocks[held] = pos; }
      table();
      var tint = [col.accent, col.text, col.muted];
      blocks.forEach(function (b, k) {
        ctx.fillStyle = tint[k]; ctx.fillRect(b[0] - 14, b[1], 28, 28);
        ctx.strokeStyle = col.surface; ctx.lineWidth = 2; ctx.strokeRect(b[0] - 14, b[1], 28, 28);
      });
      arm(376, 232, pos[0], pos[1], true);
    };

    var scenes = { research: research, projects: projects, outreach: outreach };
    var width = 0;
    var draw = function (t) {
      var w = cv.clientWidth;
      if (!w || !scenes[scene]) { return; }
      if (w !== width) {
        var dpr = Math.min(2, window.devicePixelRatio || 1);
        cv.width = Math.round(w * dpr); cv.height = Math.round(w * H / W * dpr); width = w;
      }
      readColours();
      ctx.setTransform(cv.width / W, 0, 0, cv.width / W, 0, 0);
      ctx.clearRect(0, 0, W, H);
      ctx.translate(0, -22); /* the scenes were drawn for a taller box */
      scenes[scene](t);
    };
    cv.drawAt = draw; /* lets one frame be drawn by hand, e.g. cv.drawAt(3) */
    var running = false, visible = true;
    var tick = function (now) {
      if (!running) { return; }
      draw(now / 1000);
      window.requestAnimationFrame(tick);
    };
    var update = function () {
      var head = root.getAttribute("data-head");
      var on = head === "4" || (head === "2" && cv.closest(".head-anim-right"));
      if (on && reduce) { draw(3.4); return; }
      var should = on && visible;
      if (should && !running) { running = true; window.requestAnimationFrame(tick); }
      if (!should) { running = false; }
      if (on) { draw(window.performance.now() / 1000); }
    };
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; update(); }).observe(cv);
    }
    if ("MutationObserver" in window) {
      new MutationObserver(update).observe(root, { attributes: true, attributeFilter: ["data-head", "data-theme"] });
    }
    update();
  });

  /* direction switcher (temporary, review only) */
  var buttons = document.querySelectorAll(".dirs button");
  var setDir = function (d) {
    root.setAttribute("data-dir", d);
    try { localStorage.setItem("dir", d); } catch (e) {}
    buttons.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.dir === d); });
  };
  if (buttons.length) {
    buttons.forEach(function (b) { b.addEventListener("click", function () { setDir(b.dataset.dir); }); });
    setDir(root.getAttribute("data-dir") || "a");
  }
})();
