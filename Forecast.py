import requests


class OpenWeatherMapForecasts:
    def __init__(self):
        print("2. Initialize the new instance of Point.")
        from app import app
        self.token = app.config['OWM_KEY']

    def get_current_by_lat_lon(self,lat,lon):
        url = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&appid=" + self.token \
              + "&units=metric"
        response = requests.get(url)
        return response.json()

    def get_forecast_by_lat_lon(self, lat, lon):
        url = "https://api.openweathermap.org/data/2.5/forecast?lat=" + lat + "&lon=" + lon + "&appid=" + self.token \
              + "&units=metric"
        response = requests.get(url)
        return response.json()