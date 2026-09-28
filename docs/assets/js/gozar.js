/*
 * Small enhancements for «گذار». No external requests, no tracking.
 * - Share button: uses the phone's native share sheet when available,
 *   otherwise shows links for Telegram, WhatsApp, X, email and "copy link".
 */
(function () {
  "use strict";

  var isEnglish = function () {
    return (document.documentElement.lang || "").indexOf("en") === 0;
  };

  function toast(message) {
    var el = document.createElement("div");
    el.className = "gozar-toast";
    el.setAttribute("role", "status");
    el.textContent = message;
    document.body.appendChild(el);
    setTimeout(function () {
      el.remove();
    }, 2500);
  }

  function copy(text) {
    var done = function () {
      toast(isEnglish() ? "Link copied" : "پیوند کپی شد");
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, function () {
        window.prompt("", text);
      });
    } else {
      window.prompt("", text);
    }
  }

  function shareData(button) {
    var title = (button && button.getAttribute("data-title")) || document.title;
    return { title: title, text: title, url: window.location.href.split("#")[0] };
  }

  function fillMenu(menu, data) {
    var url = encodeURIComponent(data.url);
    var text = encodeURIComponent(data.title);
    var targets = {
      telegram: "https://t.me/share/url?url=" + url + "&text=" + text,
      whatsapp: "https://wa.me/?text=" + text + "%20" + url,
      x: "https://x.com/intent/post?url=" + url + "&text=" + text,
      email: "mailto:?subject=" + text + "&body=" + url
    };
    Array.prototype.forEach.call(menu.querySelectorAll("[data-share-target]"), function (a) {
      a.href = targets[a.getAttribute("data-share-target")];
      if (a.getAttribute("data-share-target") !== "email") {
        a.target = "_blank";
      }
    });
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-share]");
    if (button) {
      var data = shareData(button);
      if (navigator.share) {
        navigator.share(data).catch(function () {});
        return;
      }
      var menu = document.querySelector(".gozar-share-menu");
      if (menu) {
        fillMenu(menu, data);
        menu.hidden = !menu.hidden;
      } else {
        copy(data.url);
      }
      return;
    }
    if (event.target.closest("[data-share-copy]")) {
      copy(window.location.href.split("#")[0]);
    }
  });
})();
