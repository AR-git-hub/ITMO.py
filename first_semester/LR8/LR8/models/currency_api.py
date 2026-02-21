import requests
import json
import os
from datetime import datetime, timedelta

BASE_URL = "https://www.cbr-xml-daily.ru"

HISTORY_FILE = "models/history_cache.json"
DAY_FILE = "models/day_cache.json"


# ============================================================
#   ЗАГРУЗКА КЭША ИЗ ФАЙЛА
# ============================================================

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ДИСКОВЫЙ КЭШ (живёт между перезапусками Python)
HISTORY_CACHE = load_json(HISTORY_FILE)
DAY_CACHE = load_json(DAY_FILE)



# ============================================================
#   ТЕКУЩИЕ КУРСЫ ВСЕХ ВАЛЮТ
# ============================================================

def get_currencies():
    url = f"{BASE_URL}/daily_json.js"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    return {code: info["Value"] for code, info in data.get("Valute", {}).items()}



# ============================================================
#   ИСТОРИЯ КУРСА
# ============================================================

def get_currency_history(code: str, date_from: str, date_to: str):
    code = code.upper()
    cache_key = f"{code}:{date_from}:{date_to}"

    if cache_key in HISTORY_CACHE:
        return HISTORY_CACHE[cache_key]

    start = datetime.strptime(date_from, "%d/%m/%Y")
    end = datetime.strptime(date_to, "%d/%m/%Y")
    delta = timedelta(days=1)

    result = []
    errors = 0  # если 5 дней подряд не получили данные — прерываем

    while start <= end:
        day_key = start.strftime("%Y-%m-%d")

        # если архив уже в кэше — не скачиваем
        if day_key in DAY_CACHE:
            data = DAY_CACHE[day_key]
        else:
            url = f"{BASE_URL}/archive/{start.year}/{start.month:02d}/{start.day:02d}/daily_json.js"
            try:
                resp = requests.get(url, timeout=0.5)  # в 6 раз быстрее
                data = resp.json() if resp.status_code == 200 else None
            except:
                data = None

            DAY_CACHE[day_key] = data
            save_json(DAY_FILE, DAY_CACHE)

        # обработка данных
        if data and "Valute" in data and code in data["Valute"]:
            rate = data["Valute"][code]["Value"]
            result.append({
                "date": day_key,
                "rate": rate
            })
            errors = 0
        else:
            errors += 1

        # если 5 дней подряд нет данных → архив закончился → выходим
        if errors >= 5:
            break

        start += delta

    HISTORY_CACHE[cache_key] = result
    save_json(HISTORY_FILE, HISTORY_CACHE)

    return result
