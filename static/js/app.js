if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker
        .register("/static/js/serviceworker.js")
        .then(() => console.log("service worker registered"))
        .catch((err) => console.log("service worker not registered", err));
    });
  }
  
// Service Worker (keep if you want)
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/static/js/serviceworker.js")
      .then(() => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}

// Review dropdown toggles
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".review-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const reviewText = btn.nextElementSibling; // should be .review-text
      if (!reviewText) return;

      const isOpen = getComputedStyle(reviewText).display !== "none";

      if (isOpen) {
        reviewText.style.display = "none";
        btn.textContent = "▼ Read review";
      } else {
        reviewText.style.display = "block";
        btn.textContent = "▲ Hide review";
      }
    });
  });
});
