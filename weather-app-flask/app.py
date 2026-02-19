from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

API_KEY = "3c07b78c6f2b2ca5d67325973839c4e4"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
def get_weather():
    city = request.args.get("city")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    return jsonify({
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "icon": data["weather"][0]["icon"]
    })


if __name__ == "__main__":
    app.run(debug=True)
