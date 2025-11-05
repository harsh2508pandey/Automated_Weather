from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Directly set your API key
API_KEY = "ff3ad8d7cf58cc6158e58bd27f1180a3"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    
    # Request weather data from OpenWeatherMap
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={'q': city, 'appid': API_KEY, 'units': 'metric'}
    )

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description'].capitalize()
        return f"🌤 Weather in {city}: {temp}°C, {desc}"
    else:
        return f"Error fetching weather for {city}: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
