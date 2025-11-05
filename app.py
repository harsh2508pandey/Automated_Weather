from flask import Flask, render_template, request
import requests
import boto3
import botocore.exceptions

app = Flask(__name__)

# ✅ Fetch API key securely from AWS SSM Parameter Store
def get_api_key():
    try:
        ssm = boto3.client('ssm', region_name='ap-south-1')
        parameter = ssm.get_parameter(Name='/automated_weather/OPENWEATHER_API_KEY', WithDecryption=True)
        return parameter['Parameter']['Value']
    except botocore.exceptions.ClientError as e:
        print("❌ Error fetching API key from SSM:", e)
        return None

# ✅ Fetch the API key once at app startup
API_KEY = get_api_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city'].strip()

    if not city:
        return "⚠️ Please enter a valid city name."

    if not API_KEY:
        return "❌ Error: API key not available. Please check your AWS SSM configuration."

    try:
        # ✅ Request weather data from OpenWeatherMap
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={'q': city, 'appid': API_KEY, 'units': 'metric'},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            return f"""
            🌤 <b>Weather in {city}</b><br>
            🌡 Temperature: {temp}°C<br>
            💧 Humidity: {humidity}%<br>
            🌬 Wind Speed: {wind_speed} m/s<br>
            🌈 Condition: {desc}
            """
        else:
            return f"❌ Unable to fetch weather for <b>{city}</b>. API responded with: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"⚠️ Network error while fetching weather: {str(e)}"

if __name__ == '__main__':
    # ✅ Run Flask on all interfaces, port 5000 (can change to 80 for public HTTP)
    app.run(host='0.0.0.0', port=5000)
