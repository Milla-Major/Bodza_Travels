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

    results.innerHTML = "Loading...";

    try {
      const res = await fetch(`/search?city=${encodeURIComponent(city)}`);
      const data = await res.json();

      if (data.error) {
        results.innerHTML = `<p class="error">${data.error}</p>`;
        return;
      }

      const places = data.features || [];
      if (places.length === 0) {
        results.innerHTML = "<p>No attractions found in this city :(</p>";
        return;
      }

      results.innerHTML = "<ul>" +
        places.map(p => `<li><strong>${p.properties.name || "Unnamed place"}</strong><br>${p.properties.address_line1 || ""}</li>`).join("") +
        "</ul>";

    } catch (err) {
      results.innerHTML = `<p class="error">Something went wrong. Please try again.</p>`;
      console.error(err);
    }
  });
});
document.addEventListener("click", function(e) {
  if (!e.target.closest(".autocomplete-container")) {
    document.getElementById("autocomplete-list").innerHTML = "";
  }
});

