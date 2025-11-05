from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "ff3ad8d7cf58cc6158e58bd27f1180a3"

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={'q': city, 'appid': API_KEY, 'units': 'metric'}
    )
    data = response.json()

    if response.status_code == 200 and "main" in data:
        result = {
            "city": city,
            "temp": data['main']['temp'],
            "description": data['weather'][0]['description'].capitalize(),
            "humidity": data['main']['humidity'],
            "wind": data['wind']['speed'],
            "icon": data['weather'][0]['icon']
        }
        return jsonify(result)
    else:
        return jsonify({"error": "City not found or API error"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
