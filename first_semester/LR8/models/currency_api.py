import requests
from typing import Dict

def get_currencies(url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Dict[str, float]:
    """
    Получает все курсы валют с API ЦБ РФ.

    Возвращает словарь вида: {'USD': 73.45, 'EUR': 85.67, ...}
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API недоступно: {e}")

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f"Некорректный JSON: {e}")

    if "Valute" not in data:
        raise KeyError("Ключ 'Valute' отсутствует в данных API")

    result = {}
    for code, info in data["Valute"].items():
        value = info.get("Value")
        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(value)}")
        result[code] = value

    return result

# Пример вызова:
# print(get_currencies())
