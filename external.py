import requests
from requests.exceptions import RequestException
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#https://www.tariffnumber.com/services/api
TARIFF_NUMBER_URL = "https://www.tariffnumber.com/api/v1/cnSuggest"

def get_tariff_number(code):
    params = {"term": code, "lang": "en", "year": "2024"}

    try:
        response = requests.get(TARIFF_NUMBER_URL, params=params, timeout=5)
        response.raise_for_status()
    except RequestException as e:
        logger.error(f"Сторонний сервис тариков умер, не могу получить номер,{e}")
        raise
    try:
        return response.json()
    except ValueError as e:
        logger.error(f"Невозможно распарсить ответ {e}")
        raise
