document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("cityForm");
  const input = document.getElementById("cityInput");
  const results = document.getElementById("placesList");
  const suggestionBox = document.getElementById("autocomplete-list");

  input.addEventListener("input", async () => {
    const query = input.value.trim();
    suggestionBox.innerHTML = "";
    if (!query) return;
    try {
      const res = await fetch(`/autocomplete?text=${encodeURIComponent(query)}`);
      const data = await res.json();
      (data.features || []).forEach(place => {
        const div = document.createElement("div");
        div.textContent = place.properties.formatted;
        div.addEventListener("click", () => {
          input.value = place.properties.city || place.properties.name || place.properties.formatted;
          suggestionBox.innerHTML = "";
        });
        suggestionBox.appendChild(div);
      });
    } catch (err) {
      console.error("Autocomplete error", err);
    }
  });
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const city = input.value.trim();
    suggestionBox.innerHTML = "";

    if (!city) return;
    window.location.href = `/results?city=${encodeURIComponent(city)}`;
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".autocomplete-container")) {
      suggestionBox.innerHTML = "";
    }
  });
});

