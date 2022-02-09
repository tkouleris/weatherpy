import requests
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    url = "https://api.openweathermap.org/data/2.5/forecast?id=833&appid=93265401429e6e79657b6e0b6d6acb96&units=metric"
    response = requests.get(url)
    weather = response.json()['list']
    city = response.json()['city']['name']
    country = response.json()['city']['country']
    response = []
    for i in range(len(weather)):
        print()
        sample = {}
        sample['dt'] = weather[i]['dt']
        sample['temprature'] = weather[i]['main']['temp']
        sample['humidity'] = weather[i]['main']['humidity']
        sample['description'] = weather[i]['weather'][0]['description']
        sample['icon'] = weather[i]['weather'][0]['icon']
        response.append(sample)

    # return {"results":weather}
    return {"results": {"info": {"city": city, "country": country}, "weather": response}}


if __name__ == '__main__':
    app.run()
