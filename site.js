(function () {
  var header = document.querySelector("[data-nav]");
  var toggle = document.querySelector("[data-nav-toggle]");
  var links = document.querySelector("[data-nav-links]");

  if (header && toggle && links) {
    toggle.addEventListener("click", function () {
      var isOpen = header.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });

    links.addEventListener("click", function (event) {
      if (event.target.tagName === "A") {
        header.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }
})();

(function () {
  var board = document.querySelector(".flow-board");
  var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-demo-button]"));
  var caption = document.querySelector("[data-demo-caption]");
  if (!board || !buttons.length) return;

  var captions = {
    normal: "normal mode: the raw key crosses into the agent or subprocess path",
    kv: "kv mode: only request and result cross the boundary"
  };

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      var mode = button.getAttribute("data-demo-button") || "kv";
      board.setAttribute("data-demo-mode", mode);
      buttons.forEach(function (candidate) {
        candidate.classList.toggle("is-active", candidate === button);
        candidate.setAttribute("aria-pressed", String(candidate === button));
      });
      if (caption) {
        caption.textContent = captions[mode] || captions.kv;
      }
    });
  });
})();

(function () {
  var steps = Array.prototype.slice.call(document.querySelectorAll("[data-kv-step]"));
  if (!steps.length || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var index = 0;
  window.setInterval(function () {
    steps.forEach(function (step) {
      step.classList.remove("is-active");
    });
    steps[index % steps.length].classList.add("is-active");
    index += 1;
  }, 1500);
})();

(function () {
  var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-copy]"));
  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      var value = button.getAttribute("data-copy") || "";
      var original = button.textContent;

      if (!navigator.clipboard) {
        button.textContent = "Select and copy";
        return;
      }

      navigator.clipboard.writeText(value).then(function () {
        button.textContent = "Copied";
        window.setTimeout(function () {
          button.textContent = original;
        }, 1400);
      });
    });
  });
})();

(function () {
  var items = Array.prototype.slice.call(document.querySelectorAll(".faq-item"));
  items.forEach(function (item) {
    var button = item.querySelector(".faq-question");
    var answer = item.querySelector(".faq-answer");
    if (!button || !answer) return;

    button.addEventListener("click", function () {
      var isOpen = item.classList.toggle("open");
      button.setAttribute("aria-expanded", String(isOpen));
      if (isOpen) {
        answer.removeAttribute("hidden");
      } else {
        answer.setAttribute("hidden", "");
      }
    });
  });
})();

(function () {
  var revealItems = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if (!revealItems.length) return;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) {
    revealItems.forEach(function (item) {
      item.classList.add("visible");
    });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.16 });

  revealItems.forEach(function (item) {
    observer.observe(item);
  });
})();
