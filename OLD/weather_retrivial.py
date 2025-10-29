import requests
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
ow_key = os.getenv('ow_key')

def weather_retrivial(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Erreur : {response.status_code}")
        return None

    # To access the temp value from the data dictionary:
    temp_value = data['main']['temp']
    cloud = data['clouds']['all']
    visibility = data['visibility']

    # Convert the UNIX timestamp to a readable date and time (UTC)
    sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'])
    sunset = datetime.utcfromtimestamp(data['sys']['sunset'])
    sun_time = (sunset - sunrise).total_seconds()

    print(f"temp : {temp_value}, cloud : {cloud}, visibility : {visibility}, sunset : {sunset}, sunrise : {sunrise}, sun_time : {sun_time}")
    return {
        "temp": temp_value,
        "cloud": cloud,
        "visibility": visibility,
        "sunset": sunset,
        "sunrise": sunrise,
        "sun_time": sun_time,
    }



### USAGE
# from weather_retrivial import weather_retrivial

# url = "https://api.openweathermap.org/data/2.5/weather?q=Gazipur,BD&appid={ow_key}"

# weather_retrivial(url)
