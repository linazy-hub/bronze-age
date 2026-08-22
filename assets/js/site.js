/* ==========================================================================
   Bronze Age Furniture — site.js
   Vanilla. No dependencies. Everything degrades if JS is off.
   ========================================================================== */
(function () {
  "use strict";

  /* --- safe storage (never throws in restricted contexts) ---------------- */
  var store = {
    get: function (k) { try { return window.sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.sessionStorage.setItem(k, v); } catch (e) {} }
  };

  /* --- 1. Intro overlay -------------------------------------------------- */
  function initIntro() {
    var intro = document.getElementById("intro");
    if (!intro) return;

    // Already seen this session? Never show it again.
    if (store.get("ba_intro_seen") === "1") {
      intro.parentNode.removeChild(intro);
      return;
    }

    intro.hidden = false;
    document.body.classList.add("is-locked");

    function close() {
      intro.classList.add("is-closing");
      document.body.classList.remove("is-locked");
      store.set("ba_intro_seen", "1");
      window.setTimeout(function () {
        if (intro.parentNode) intro.parentNode.removeChild(intro);
      }, 750);
    }

    intro.addEventListener("click", function (e) {
      if (e.target.closest("[data-intro-close]")) { e.preventDefault(); close(); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("is-locked")) close();
    });

    // Closing after a successful signup feels right.
    intro.addEventListener("ba:signup", function () { window.setTimeout(close, 1400); });
  }

  /* --- 2. Newsletter + contact forms ------------------------------------- */
  var RE_EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function initForms() {
    document.addEventListener("submit", function (e) {
      var form = e.target;
      if (!form.matches("[data-signup]") && !form.matches("[data-enquiry]")) return;
      e.preventDefault();

      var note = form.querySelector(".form-note");
      var email = form.querySelector('input[type="email"]');

      function say(msg, kind) {
        if (!note) return;
        note.textContent = msg;
        note.className = "form-note" + (kind ? " is-" + kind : "");
      }

      if (email && !RE_EMAIL.test(email.value.trim())) {
        say("That email doesn't look right — mind checking it?", "err");
        email.focus();
        return;
      }

      /* ------------------------------------------------------------------
         DEMO BEHAVIOUR ONLY.
         Replace this block with a real POST to your list provider, e.g.

           fetch("https://your-endpoint", {
             method: "POST",
             headers: { "Content-Type": "application/json" },
             body: JSON.stringify(Object.fromEntries(new FormData(form)))
           })

         Mailchimp, Buttondown, ConvertKit and Formspree all accept this.
      ------------------------------------------------------------------ */
      if (form.matches("[data-signup]")) {
        say("You're in. Watch your inbox.", "ok");
      } else {
        say("Thank you — we'll reply within two working days.", "ok");
      }
      form.reset();
      form.dispatchEvent(new CustomEvent("ba:signup", { bubbles: true }));
    });
  }

  /* --- 3. Mobile nav ----------------------------------------------------- */
  function initNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var nav = document.getElementById("primary-nav");
    if (!toggle || !nav) return;
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
  }

  /* --- 4. Sticky header hairline ----------------------------------------- */
  function initHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var tick = function () {
      header.classList.toggle("is-stuck", window.scrollY > 8);
    };
    tick();
    window.addEventListener("scroll", tick, { passive: true });
  }

  /* --- 5. Reveal on scroll ----------------------------------------------- */
  function initReveal() {
    var els = document.querySelectorAll(".reveal");
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) {
      els.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var delay = parseFloat(el.getAttribute("data-delay") || "0");
        window.setTimeout(function () { el.classList.add("is-in"); }, delay * 1000);
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* --- 6. Shop filters --------------------------------------------------- */
  function initFilters() {
    var bar = document.querySelector("[data-filters]");
    if (!bar) return;
    var items = Array.prototype.slice.call(document.querySelectorAll("[data-category]"));
    var count = bar.querySelector(".filters__count");

    function apply(cat) {
      var shown = 0;
      items.forEach(function (item) {
        var match = cat === "all" || item.getAttribute("data-category") === cat;
        item.style.display = match ? "" : "none";
        if (match) shown++;
      });
      if (count) count.textContent = shown + (shown === 1 ? " piece" : " pieces");
      bar.querySelectorAll("button").forEach(function (b) {
        b.classList.toggle("is-active", b.getAttribute("data-filter") === cat);
      });
      try {
        history.replaceState(null, "", cat === "all" ? location.pathname : "#" + cat);
      } catch (e) {}
    }

    bar.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-filter]");
      if (btn) apply(btn.getAttribute("data-filter"));
    });

    var initial = (location.hash || "").replace("#", "") || "all";
    apply(bar.querySelector('[data-filter="' + initial + '"]') ? initial : "all");
  }

  /* --- boot -------------------------------------------------------------- */
  function boot() {
    initIntro();
    initForms();
    initNav();
    initHeader();
    initReveal();
    initFilters();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
