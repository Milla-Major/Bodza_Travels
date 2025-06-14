document.addEventListener("DOMContentLoaded", () => {
  const items = document.querySelectorAll(".recent-list li");
  const seen = new Set();

  items.forEach(item => {
    const nameElement = item.querySelector("strong");
    if (!nameElement) return;

    const name = nameElement.textContent.trim().toLowerCase();
    if (seen.has(name)) {
      item.remove();  
    } else {
      seen.add(name);
    }
  });
});
