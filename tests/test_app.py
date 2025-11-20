import json
from app import app

def test_home_page():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200

def test_weather_api():
    tester = app.test_client()
    response = tester.get('/weather?city=London')
    assert response.status_code in [200, 400]

    # If API works
    if response.status_code == 200:
        data = json.loads(response.data.decode('utf-8'))
        assert 'temperature' in data
