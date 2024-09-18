from enum import Enum
from dotenv import dotenv_values

api_key = dotenv_values(".env")['GOOGLE-API-KEY']


class ApiKey(Enum):
    API_KEY = api_key
