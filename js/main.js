/* Runs before first paint (script sits at end of body, not deferred). */
document.documentElement.classList.add("js");

/* ORIENTATION: threshold doors part once per session; any tap skips. */
(function () {
  var doors = document.querySelector(".gate-split, .threshold");
  if (!doors) return;
  var seen;
  try { seen = sessionStorage.getItem("srp-oriented"); } catch (e) {}
  if (seen) return;
  var html = document.documentElement;
  html.classList.add("orienting");
  try { sessionStorage.setItem("srp-oriented", "1"); } catch (e) {}
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { html.classList.remove("orienting"); });
  });
  document.addEventListener("pointerdown", function () { html.classList.remove("orienting"); }, { once: true });
})();

document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll(".path-switch button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var path = btn.getAttribute("data-set");
      document.documentElement.dataset.path = path;
      try { localStorage.setItem("srp-path", path); } catch (e) {}
    });
  });

  /* ORIENTATION (part 2): confluence draws once per session. */
  var motif = document.querySelector(".confluence");
  if (motif) {
    var flowed;
    try { flowed = sessionStorage.getItem("srp-flow"); } catch (e) {}
    if (!flowed) {
      motif.classList.add("animate");
      try { sessionStorage.setItem("srp-flow", "1"); } catch (e) {}
    }
  }

  /* CONTINUITY: surfaces rise on first view; once; stagger <= 3 x 80ms. */
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var surfaces = document.querySelectorAll(".card, .step, .post-card");
  if (!reduce && "IntersectionObserver" in window) {
    var i = 0;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        io.unobserve(el);
        var delay = (i % 3) * 80;
        i++;
        setTimeout(function () { el.classList.add("risen"); }, delay);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    surfaces.forEach(function (el) { el.classList.add("rise"); io.observe(el); });
  }

  /* Booking form confirmation state. */
  if (location.search.indexOf("sent=1") > -1) {
    var form = document.getElementById("consult-form");
    var sent = document.getElementById("form-sent");
    if (form && sent) {
      form.hidden = true;
      sent.hidden = false;
      var book = document.getElementById("book");
      if (book) book.scrollIntoView();
    }
  }
});
