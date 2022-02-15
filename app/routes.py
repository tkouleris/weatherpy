from app import app
from app.models import City
import requests


@app.route('/<city_id>')
def getForecast(city_id):
    print('getForecast')
    city = City.query.filter_by(id=city_id).first()
    print(city.owm_id)
    url = "https://api.openweathermap.org/data/2.5/forecast?id=" + str(city.owm_id) + "&appid=" + app.config[
        'OWM_KEY'] + "&units=metric"
    response = requests.get(url)
    weather = response.json()['list']
    city = response.json()['city']['name']
    country = response.json()['city']['country']
    response = []
    for i in range(len(weather)):
        sample = {
            'dt': weather[i]['dt'],
            'temperature': weather[i]['main']['temp'],
            'humidity': weather[i]['main']['humidity'],
            'description': weather[i]['weather'][0]['description'],
            'icon': weather[i]['weather'][0]['icon']}
        response.append(sample)

    return {"results": {"info": {"city": city, "country": country}, "weather": response}}
