import os

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv('CURRENCY_API')


async def get_conversion(data: dict):
    """
    Обращаемся к API с конвертацией валют
    """

    to_currency = data['to']
    from_currency = data['from']
    amount = data['amount']
    async with ClientSession() as session:
        url = 'https://api.apilayer.com/currency_data/convert'
        params = {'to': to_currency, 'from': from_currency, 'amount': amount,
                  'apikey': API_KEY}
        try:
            async with session.get(url=url, params=params) as response:
                currency_json = await response.json()
                return currency_json
        except Exception as ex:
            return {'error': 'server_error', 'error_ex': ex}