import requests, os, sqlite3, json
from flask import Flask, render_template, request, jsonify, redirect, flash
from dotenv import load_dotenv
from database import get_recent_places, save_search
# I used the flask documentation and the course materials to learn how to set up the app correctly
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
GEOAPIFY_KEY = os.getenv("GEOAPIFY_KEY")
DB_PATH = "data/btravels.db"


with open("category_map.json", "r", encoding="utf-8") as f:
    CATEGORY_MAP = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/recent_places")
def recent_places():
    places = get_recent_places()
    return render_template("recent_places.html", places=places)


@app.route("/support")
def support():
    return render_template("support.html")

@app.route("/submit-support", methods=["POST"])
def submit_support():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not (name and email and message):
        flash("All fields are required.", "error")
        return redirect("/support")

    print(f"New support message from {name} <{email}>: {message}")

    return render_template("support_submitted.html", name=name)


@app.route("/results") #I used the help of chatgpt to make this function work correctly
def results():
    city_name = request.args.get("city")
    if not city_name:
        return render_template("results.html", error="No city name provided.")

    try:
        save_search(city_name)
        geo_url = "https://api.geoapify.com/v1/geocode/search"
        geo_params = {"text": city_name, "apiKey": GEOAPIFY_KEY}
        geo_res = requests.get(geo_url, params=geo_params)
        geo_res.raise_for_status()
        geo_data = geo_res.json()

        if not geo_data.get("features"):
            return render_template("results.html", error=f"No location found for '{city_name}'.")

        coords = geo_data["features"][0]["geometry"]["coordinates"]
        if not coords or len(coords) != 2:
            return render_template("results.html", error="Invalid location coordinates received.")

        lon, lat = coords[0], coords[1]

        place_url = "https://api.geoapify.com/v2/places"
        place_params = {
            "categories": "tourism.sights",
            "filter": f"circle:{lon},{lat},5000",
            "limit": 50,
            "apiKey": GEOAPIFY_KEY
        }
        place_res = requests.get(place_url, params=place_params)
        place_res.raise_for_status()
        place_data = place_res.json()

        raw_sights = place_data.get("features", [])
        if not raw_sights:
            return render_template("results.html", city=city_name, sights=[], message="No sights found in this city.")
        #dupl
        seen = set()
        unique_sights = []
        for s in raw_sights:
            props = s.get("properties", {})
            geom = s.get("geometry", {})
            name = props.get("name", "").strip().lower()
            addr = props.get("address_line1", "").strip().lower()
            coords = tuple(round(c, 5) for c in geom.get("coordinates", []))
            #categories = tuple(sorted(props.get("categories", [])))
            categories_raw = props.get("categories", [])
            categories = tuple(sorted(categories_raw))
            simple_categories = list({CATEGORY_MAP.get(cat, cat.split(".")[-1]) for cat in categories_raw})
            props["simple_categories"] = simple_categories
            key = (name, addr, coords, categories)
            if name and key not in seen:
                seen.add(key)
                unique_sights.append(s)

        return render_template("results.html", city=city_name, sights=unique_sights)

    except requests.exceptions.HTTPError as http_err:
        return render_template("results.html", error=f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        return render_template("results.html", error="Network error: Failed to connect to Geoapify API.")
    except requests.exceptions.Timeout:
        return render_template("results.html", error="Request to Geoapify timed out.")
    except requests.exceptions.RequestException as req_err:
        return render_template("results.html", error=f"Request error: {req_err}")
    except Exception as e:
        return render_template("results.html", error=f"Unexpected error: {str(e)}")


@app.route("/autocomplete") #help from Geoapify docs
def autocomplete():
    query = request.args.get("text")
    if not query:
        return jsonify([])

    try:
        geo_url = "https://api.geoapify.com/v1/geocode/autocomplete"
        params = {"text": query, "limit": 5, "apiKey": GEOAPIFY_KEY }
        response = requests.get(geo_url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
