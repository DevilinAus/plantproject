from dotenv import load_dotenv
import requests
import os

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Brisbane"

outbound_request = (
    f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"
)

response = requests.get(outbound_request)


def get_weather():
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Failed to fetch data: {response.status_code}")


get_weather()
