from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Your OpenWeatherMap API Key
API_KEY = "0089a5613761094cad0055cbe2c01cb0"
BACKGROUND_IMAGES = [
    "https://source.unsplash.com/random/1600x900/?weather,sun",
    "https://source.unsplash.com/random/1600x900/?weather,rain",
    "https://source.unsplash.com/random/1600x900/?weather,clouds",
    "https://source.unsplash.com/random/1600x900/?weather,snow",
    "https://source.unsplash.com/random/1600x900/?weather,storm"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None
    bg_image = random.choice(BACKGROUND_IMAGES)
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                
                data = response.json()
                weather = {
                    'city': data['name'],
                    'temp': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind': data['wind']['speed']
                }
            except requests.exceptions.RequestException as e:
                error = f"Error getting weather: {e}"
            except (KeyError, IndexError) as e:
                error = f"Invalid data received: {e}"
    
    return render_template('index.html', 
                        weather=weather, 
                        error=error,
                        bg_image=bg_image)

if __name__ == '__main__':
    app.run(debug=True)