(function () {
  // Sticky bar: hide while the hero buttons or the final button are on screen.
  var bar = document.getElementById("sticky-bar");
  var watch = [document.getElementById("hero-actions"), document.querySelector("[data-final-cta]")];
  if (bar && "IntersectionObserver" in window) {
    var visible = new Set();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) visible.add(en.target); else visible.delete(en.target);
      });
      bar.classList.toggle("is-hidden", visible.size > 0);
    });
    watch.forEach(function (el) { if (el) io.observe(el); });
  }

  // TikTok facade: load the official embed only after a tap.
  var facade = document.querySelector(".facade[data-video-id]");
  if (facade) {
    facade.addEventListener("click", function (ev) {
      ev.preventDefault();
      var id = facade.getAttribute("data-video-id");
      var quote = document.createElement("blockquote");
      quote.className = "tiktok-embed";
      quote.setAttribute("cite", facade.getAttribute("data-cite"));
      quote.setAttribute("data-video-id", id);
      quote.style.cssText = "max-width:325px;min-width:290px;margin:0 auto";
      quote.innerHTML = "<section></section>";
      facade.replaceWith(quote);
      var s = document.createElement("script");
      s.src = "https://www.tiktok.com/embed.js";
      s.async = true;
      document.body.appendChild(s);
    });
  }
})();
