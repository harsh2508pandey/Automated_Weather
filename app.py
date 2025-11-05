from flask import Flask, render_template, request, jsonify
import requests, os

app = Flask(__name__, template_folder='templates')

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City is required"}), 400

    if not OPENWEATHER_API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric'

    try:
        res = requests.get(url)
        data = res.json()
        if res.status_code != 200:
            return jsonify({"error": data.get("message", "Error fetching data")}), res.status_code

        return jsonify({
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
