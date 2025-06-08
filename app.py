import requests, os, sqlite3
from flask import Flask, render_template, request, jsonify, redirect, flash
from dotenv import load_dotenv
from database import get_recent_places, save_search

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
GEOAPIFY_KEY = os.getenv("GEOAPIFY_KEY")
DB_PATH = "data/btravels.db"

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

@app.route("/search")
def search():
    raw_city = request.args.get("city_name", "")
    city_name = raw_city.strip().title() 
    if not city_name:
        return jsonify({"error": "Please enter a city name."}), 400
    try:
        save_search(city_name)
    except Exception as e:
        return jsonify({"error": "Failed to save search.", "details": str(e)}), 500

    try:
        geo_url = "https://api.geoapify.com/v1/geocode/search"
        geo_params = {"text": city_name, "apiKey": GEOAPIFY_KEY}
        geo_res = requests.get(geo_url, params=geo_params)
        geo_data = geo_res.json()

        lat = geo_data["features"][0]["geometry"]["coordinates"][1]
        lon = geo_data["features"][0]["geometry"]["coordinates"][0]
    except (KeyError, IndexError):
        return jsonify({"error": f"Could not find location: '{city_name}'"}), 404
    except Exception as e:
        return jsonify({"error": "Error while geocoding", "details": str(e)}), 500

    try:
        place_url = "https://api.geoapify.com/v2/places"
        place_params = {
            "categories": "tourism.sights",
            "filter": f"circle:{lon},{lat},5000",
            "limit": 20,
            "apiKey": GEOAPIFY_KEY
        }
        place_res = requests.get(place_url, params=place_params)
        place_res.raise_for_status()
        places = place_res.json()
    except Exception as e:
        return jsonify({"error": "Could not retrieve places.", "details": str(e)}), 500

    return jsonify(places)

@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("text")
    if not query:
        return jsonify([])

    try:
        geo_url = "https://api.geoapify.com/v1/geocode/autocomplete"
        params = {
            "text": query,
            "limit": 5,
            "apiKey": GEOAPIFY_KEY
        }
        response = requests.get(geo_url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
