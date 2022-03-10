import requests

from app import app


def forecast_fetcher_factory():
    if app.config['ENV'] == 'testing':
        return MockForecastFetcher()
    else:
        return ForecastFetcherImpl()


class ForecastFetcherImpl:

    def __init__(self):
        self.api_key = app.config['OWM_KEY']

    def getForecast(self, city_id):
        url = "https://api.openweathermap.org/data/2.5/forecast?id=" + str(city_id) + "&appid=" + app.config[
            'OWM_KEY'] + "&units=metric"
        response = requests.get(url)
        weather = response.json()['list']
        city = response.json()['city']['name']
        country = response.json()['city']['country']
        response = []
        forecast = []
        for i in range(len(weather)):
            sample = {
                'dt': weather[i]['dt'],
                'temperature': weather[i]['main']['temp'],
                'humidity': weather[i]['main']['humidity'],
                'description': weather[i]['weather'][0]['description'],
                'icon': weather[i]['weather'][0]['icon']}
            response.append(sample)
        forecast.append({"info": {"city": city, "country": country}, "weather": response})
        return forecast


class MockForecastFetcher:

    def getForecast(self, city_id):
        city = 'Gotham'
        country = 'USA'
        response = []
        forecast = []
        sample = {
            'dt': 1,
            'temperature': 10,
            'humidity': 60,
            'description': 'cloudy',
            'icon': 'cloud_icon'
        }
        response.append(sample)
        forecast.append({"info": {"city": city, "country": country}, "weather": response})
        return forecast
