import numpy as np

def fft(data):

  return np.fft.fft(data)

  
  import aiohttp
import aiofiles
import asyncio
import json
from datetime import datetime

class WeatherFetcher:
    def __init__(self, api_key, base_url="http://api.openweathermap.org/data/2.5/weather"):
        self.api_key = api_key
        self.base_url = base_url

    async def fetch_weather(self, city):
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    response.raise_for_status()

    async def save_weather_data(self, city, data):
        filename = f"{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        async with aiofiles.open(filename, 'w') as file:
            await file.write(json.dumps(data, indent=4))
        print(f"Weather data saved to {filename}")

    def parse_weather_data(self, data):
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

    async def get_and_save_weather(self, city):
        try:
            data = await self.fetch_weather(city)
            weather_report = self.parse_weather_data(data)
            print(f"Weather in {city}:\n{weather_report}")
            await self.save_weather_data(city, data)
        except Exception as e:
            print(f"Error fetching weather data for {city}: {e}")

