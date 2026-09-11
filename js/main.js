/* ==========================================================================
   TheGateKeeper.art — main.js
   Vanilla, no dependencies. Progressive: the page works fine without JS.
   ========================================================================== */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 1. Sticky nav shadow ---------- */
  var nav = document.getElementById("nav");
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle("is-stuck", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- 2. Mobile menu ---------- */
  var toggle = document.getElementById("navToggle");
  var links = document.getElementById("navLinks");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });

    links.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- 3. Reveal on scroll ---------- */
  var revealables = document.querySelectorAll(".reveal");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    for (var i = 0; i < revealables.length; i++) revealables[i].classList.add("is-visible");
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          var siblings = Array.prototype.slice.call(
            el.parentElement ? el.parentElement.querySelectorAll(".reveal") : []
          );
          var idx = Math.min(siblings.indexOf(el), 6);
          el.style.transitionDelay = Math.max(0, idx) * 70 + "ms";
          el.classList.add("is-visible");
          io.unobserve(el);
        });
      },
      { rootMargin: "0px 0px -12% 0px", threshold: 0.08 }
    );
    for (var j = 0; j < revealables.length; j++) io.observe(revealables[j]);
  }

  /* ---------- 4. Gallery filter ---------- */
  var filters = document.querySelectorAll("[data-filter]");
  var pieces = document.querySelectorAll(".piece");

  filters.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var want = btn.dataset.filter;

      filters.forEach(function (b) {
        b.classList.toggle("is-active", b === btn);
        b.setAttribute("aria-pressed", String(b === btn));
      });

      pieces.forEach(function (piece) {
        var show = want === "all" || piece.dataset.cat === want;
        piece.classList.toggle("is-hidden", !show);
        if (show) {
          /* re-run the reveal animation for freshly shown cards */
          piece.classList.remove("is-visible");
          void piece.offsetWidth;
          piece.classList.add("is-visible");
        }
      });
    });
  });

  /* ---------- 5. Lightbox ---------- */
  var lightbox = document.getElementById("lightbox");
  var lbImg = document.getElementById("lightboxImg");
  var lbTitle = document.getElementById("lightboxTitle");
  var lbMeta = document.getElementById("lightboxMeta");
  var lbClose = document.getElementById("lightboxClose");
  var lastFocus = null;

  function openLightbox(piece) {
    var img = piece.querySelector("img");
    if (!img || !lightbox) return;

    lastFocus = document.activeElement;
    lbImg.src = img.currentSrc || img.src;
    lbImg.alt = img.alt;
    lbTitle.textContent = (piece.querySelector("h3") || {}).textContent || "";
    lbMeta.textContent = (piece.querySelector("dl") || {}).textContent || "";

    lightbox.hidden = false;
    /* next frame so the transition runs */
    window.requestAnimationFrame(function () {
      lightbox.classList.add("is-open");
    });
    document.body.style.overflow = "hidden";
    if (lbClose) lbClose.focus();
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove("is-open");
    document.body.style.overflow = "";
    window.setTimeout(function () {
      lightbox.hidden = true;
      lbImg.src = "";
    }, reduceMotion ? 0 : 280);
    if (lastFocus) lastFocus.focus();
  }

  pieces.forEach(function (piece) {
    var zoom = piece.querySelector("[data-lightbox]");
    var frame = piece.querySelector(".piece__frame");

    if (zoom) zoom.addEventListener("click", function () { openLightbox(piece); });

    if (frame) {
      frame.style.cursor = "zoom-in";
      frame.addEventListener("click", function (e) {
        if (e.target.closest("[data-lightbox]")) return; /* already handled */
        openLightbox(piece);
      });
    }
  });

  if (lbClose) lbClose.addEventListener("click", closeLightbox);

  if (lightbox) {
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) closeLightbox();
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && lightbox && lightbox.classList.contains("is-open")) closeLightbox();
  });

  /* ---------- 6. Commission form ---------- */
  /* No backend: the form composes a mailto link.
     To switch to a real endpoint, set FORM_ENDPOINT below (e.g. your Formspree ID). */
  var FORM_ENDPOINT = ""; /* e.g. "https://formspree.io/f/xxxxxxxx" */
  var MAILTO = "hello@thegatekeeper.art";

  var form = document.getElementById("commissionForm");
  var status = document.getElementById("formStatus");

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var data = new FormData(form);
      var name = (data.get("name") || "").toString().trim();
      var email = (data.get("email") || "").toString().trim();
      var type = (data.get("type") || "").toString();
      var details = (data.get("details") || "").toString().trim();

      if (!name || !email || !details) {
        if (status) status.textContent = "Fill in your name, email and the idea.";
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        if (status) status.textContent = "That email doesn't look right.";
        return;
      }

      if (FORM_ENDPOINT) {
        if (status) status.textContent = "Sending…";
        fetch(FORM_ENDPOINT, {
          method: "POST",
          headers: { Accept: "application/json" },
          body: data
        })
          .then(function (res) {
            if (!res.ok) throw new Error("Request failed");
            form.reset();
            if (status) status.textContent = "Sent — you'll get a reply from the bench.";
          })
          .catch(function () {
            if (status) status.textContent = "Couldn't send. Email " + MAILTO + " instead.";
          });
        return;
      }

      var subject = "Commission enquiry — " + type;
      var body =
        "Name: " + name + "\n" +
        "Email: " + email + "\n" +
        "Type: " + type + "\n\n" +
        details + "\n";

      window.location.href =
        "mailto:" + MAILTO +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);

      if (status) status.textContent = "Opening your email app…";
    });
  }

  /* ---------- 7. Footer year ---------- */
  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
