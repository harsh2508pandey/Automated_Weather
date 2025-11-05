rom flask import Flask, render_template, request
import requests
import boto3
import botocore.exceptions

app = Flask(__name__)

# Fetch API key securely from AWS SSM Parameter Store
def get_api_key():
    try:
        ssm = boto3.client('ssm', region_name='ap-south-1')
        parameter = ssm.get_parameter(Name='/automated_weather/OPENWEATHER_API_KEY', WithDecryption=True)
        return parameter['Parameter']['Value']
    except botocore.exceptions.ClientError as e:
        print("❌ Error fetching API key from SSM:", e)
        return None

# Fetch the API key once at app startup
API_KEY = get_api_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']

    if not API_KEY:
        return "Error: API key not available. Please check your AWS SSM configuration."

    # Request weather data from OpenWeatherMap
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather",
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
    # Run Flask on all interfaces
    app.run(host='0.0.0.0', port=5000)
