from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Your OpenWeather API Key
API_KEY = "ff3ad8d7cf58cc6158e58bd27f1180a3"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City not provided"}), 400

    # OpenWeather API request
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": city,
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description'].capitalize(),
            "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
        return jsonify(weather_info)
    else:
        return jsonify({"error": f"Could not fetch weather for {city}"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
