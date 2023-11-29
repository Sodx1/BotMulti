import os

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_WEATHER_API_KEY")


async def get_weather(city):
    """
    Получение погоды
    """

    async with ClientSession() as session:
        url = ('http://api.openweathermap.org/data/2.5/weather')
        params = {'q': city, 'units': 'metric', 'lang': 'ru', 'appid': API_KEY}

        try:
            async with session.get(url=url, params=params) as response:
                weather_json = await response.json()
                return weather_json
        except Exception as ex:
            return {'cod': 'server_error', 'error_ex': ex}