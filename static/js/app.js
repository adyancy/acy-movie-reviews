if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker
        .register("/static/js/serviceworker.js")
        .then(() => console.log("service worker registered"))
        .catch((err) => console.log("service worker not registered", err));
    });
  }
  
  // Service Worker
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
      // Find the review text inside the same poster card (more reliable than nextElementSibling)
      const card = btn.closest(".poster-card");
      if (!card) return;

      const review = card.querySelector(".review-text");
      if (!review) return;

      const isOpen = review.style.display === "block";

      if (isOpen) {
        review.style.display = "none";
        btn.textContent = "▼ Read review";
      } else {
        review.style.display = "block";
        btn.textContent = "▲ Hide review";
      }
    });
  });
});
