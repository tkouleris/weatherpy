
<h1>WeatherPy App</h1>  
<p>Weather Forecast (Greece) - A Flask app that uses OpenWeatherMap to get forecasts and show it in a web page</p>  
  
## Installation  - windows
a. create a virtual environment
b. enable the virtual environment
c. install packages

    py -3 -m venv venv
    venv\Scripts\activate
	pip install -r requirements.txt
    
    
## Installation  - Linux
a. create a virtual environment
b. enable the virtual environment
c. install packages

    python3 -m venv venv
    venv/bin/activate
    pip install -r requirements.txt

## The .env file
create a .env file and fill the variables.
OWM_KEY needs a key from Open Weather Maps
IPSTACK_KEY needs a key from ipstack.com
SECRET_KEY just a random string
SQLALCHEMY_DATABASE_URI the database connection for example

    SQLALCHEMY_DATABASE_URI='mysql://root:developer@127.0.0.1:3306/weatherapp_db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

 


## Migrations

    flask db upgrade

## Run the application

    flask run


