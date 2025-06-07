document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("cityForm");
  const input = document.getElementById("cityInput");
  const results = document.getElementById("placesList");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const city = input.value.trim();
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
        results.innerHTML = "<p>No attractions found in this city:( </p>";
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
