from flask import Flask, render_template, request
import requests
from waitress import serve
from datetime import datetime
import pytz
from tzlocal import get_localzone

app = Flask(__name__)

# Configuration
API_KEY = "0089a5613761094cad0055cbe2c01cb0"
DEFAULT_CITIES = [
    "Bangalore,IN", "Guwahati,IN", "Kanpur,IN",
    "California,US", "Vellore,IN", "Boston,US",
    "Davangere,IN", "Bellary,IN"
]

WEATHER_BACKGROUNDS = {
    "Clear": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)",
    "Clouds": "linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%)",
    "Rain": "linear-gradient(135deg, #4b79cf 0%, #283e51 100%)",
    "Thunderstorm": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
    "Snow": "linear-gradient(135deg, #e6e9f0 0%, #eef1f5 100%)",
    "default": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
}

def get_weather_data(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    all_weather = []
    bg_style = WEATHER_BACKGROUNDS['default']
    searched_weather = None
    
    # Get weather for default cities
    for city in DEFAULT_CITIES:
        if data := get_weather_data(city):
            weather_main = data['weather'][0]['main']
            all_weather.append({
                'city': data['name'],
                'country': data['sys']['country'],
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'],
                'main_weather': weather_main
            })

    # Handle search
    if request.method == 'POST' and (city := request.form.get('city')):
        if data := get_weather_data(city):
            weather_main = data['weather'][0]['main']
            searched_weather = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'],
                'main_weather': weather_main
            }
            bg_style = WEATHER_BACKGROUNDS.get(weather_main, WEATHER_BACKGROUNDS['default'])

    return render_template('index.html',
                         all_weather=all_weather,
                         searched_weather=searched_weather,
                         bg_style=bg_style)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=10000)