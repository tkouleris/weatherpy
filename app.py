import os
import requests
from flask import Flask
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['OWM_KEY'] = os.getenv('OWM_KEY')


@app.route('/')
def hello_world():  # put application's code here
    url = "https://api.openweathermap.org/data/2.5/forecast?id=833&appid="+app.config['OWM_KEY']+"&units=metric"
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

    # return {"results":weather}
    return {"results": {"info": {"city": city, "country": country}, "weather": response}}


if __name__ == '__main__':
    app.run()
