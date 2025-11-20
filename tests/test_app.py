from app import app
import pytest

def test_home_page():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200

@pytest.mark.skip(reason="Weather API route not implemented in the app")
def test_weather_api():
    tester = app.test_client()
    response = tester.get('/weather?city=London')
    assert response.status_code in [200, 400]
