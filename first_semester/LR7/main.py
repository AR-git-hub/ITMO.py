import functools
import requests
import sys
from typing import Callable, Any, List, Dict
import logging
# https://chat.deepseek.com/share/zd54cka1z387b5y2iz
import math


def logger(func: Callable = None, *, handle=sys.stdout): # type: ignore
    """
    Универсальный декоратор для логирования.
    
    Использование:
    1. @logger  # handle=sys.stdout по умолчанию
    2. @logger()  # тоже handle=sys.stdout
    3. @logger(handle=sys.stderr)  # в stderr
    4. @logger(handle=io.StringIO())  # в строковый буфер
    5. @logger(handle=logging.getLogger("name"))  # в логгер
    """
    if func is None:
        return lambda f: logger(f, handle=handle)
    
    @functools.wraps(func)
    def inner(*args, **kwargs) -> Any:
        # Определяем способ логирования
        if isinstance(handle, logging.Logger):
            # Для логгера используем его методы с разными уровнями
            def log(level, msg):
                if level == 'INFO':
                    handle.info(msg) # type: ignore
                elif level == 'WARNING':
                    handle.warning(msg) # type: ignore
                elif level == 'ERROR':
                    handle.error(msg) # type: ignore
                elif level == 'CRITICAL':
                    handle.critical(msg) # type: ignore
                else:
                    handle.info(msg)  # type: ignore # по умолчанию
        else:
            # Для потока пишем с префиксом уровня
            def log(level, msg):
                handle.write(f"{level}: {msg}\n")
                if hasattr(handle, 'flush'):
                    handle.flush()
        
        # Логируем начало вызова (INFO)
        log('INFO', f"Вызов функции {func.__name__} с args={args}, kwargs={kwargs}")
        
        try:
            # Вызываем оригинальную функцию
            result = func(*args, **kwargs)
            
            # Логируем успешное завершение (INFO)
            log('INFO', f"Функция {func.__name__} завершилась успешно. Результат: {result}")
            
            return result
            
        except Exception as e:
            # Определяем уровень для ошибки по содержимому сообщения
            error_msg = str(e)
            if 'CRITICAL' in error_msg.upper():
                level = 'CRITICAL'
            elif 'WARNING' in error_msg.upper():
                level = 'WARNING'
            else:
                level = 'ERROR'
            
            # Логируем ошибку
            log(level, f"Функция {func.__name__} вызвала исключение {type(e).__name__}: {error_msg}")
            
            # Пробрасываем исключение дальше
            raise
    
    return inner


# ========================================
# ДЕМО КВАДРАТНОГО УРАВНЕНИЯ
# ============================================

@logger
def solve_quadratic(a: float, b: float, c: float):
    """
    Решает квадратное уравнение a*x^2 + b*x + c = 0
    
    Демонстрирует разные уровни логирования:
    - INFO: два корня
    - WARNING: дискриминант < 0  
    - ERROR: некорректные данные
    - CRITICAL: a=b=0
    """
    # Проверка типов (ERROR)
    if not all(isinstance(x, (int, float)) for x in [a, b, c]):
        raise TypeError("ERROR: Коэффициенты должны быть числами")
    
    # Вырожденный случай (CRITICAL)
    if a == 0 and b == 0:
        raise ValueError("CRITICAL: Оба коэффициента a и b равны 0")
    
    if a == 0:
        # Линейное уравнение (INFO)
        return [-c / b]
    
    # Вычисляем дискриминант
    d = b**2 - 4*a*c
    
    # Отрицательный дискриминант (WARNING)
    if d < 0:
        raise ValueError(f"WARNING: Дискриминант отрицательный: {d}")
    
    if d == 0:
        # Один корень (INFO)
        x = -b / (2*a)
        return [x]
    
    # Два корня (INFO)
    sqrt_d = math.sqrt(d)
    x1 = (-b + sqrt_d) / (2*a)
    x2 = (-b - sqrt_d) / (2*a)
    return [x1, x2]



# ==========================================
# get_currencies 
# ============================================

def get_currencies(
    currency_codes: List[str], 
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> Dict[str, float]:
    """
    Получает курсы валют с API ЦБ РФ.
    
    ТОЛЬКО бизнес-логика! Никакого логирования внутри!
    
    Raises:
        ConnectionError: API недоступен
        ValueError: Некорректный JSON
        KeyError: Нет ключа "Valute" или валюта отсутствует
        TypeError: Курс валюты имеет неверный тип
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверка HTTP ошибок
        
    except requests.exceptions.RequestException as e:
        # По ТЗ: API недоступен → ConnectionError
        raise ConnectionError(f"API недоступно: {e}")
    
    try:
        data = response.json()
    except ValueError as e:
        # По ТЗ: Некорректный JSON → ValueError
        raise ValueError(f"Некорректный JSON: {e}")
    
    # По ТЗ: Нет ключа "Valute" → KeyError
    if "Valute" not in data:
        raise KeyError("Ключ 'Valute' отсутствует в данных API")
    
    result = {}
    for code in currency_codes:
        # По ТЗ: Валюта отсутствует → KeyError
        if code not in data["Valute"]:
            raise KeyError(f"Валюта '{code}' отсутствует в данных API")
        
        value = data["Valute"][code]["Value"]
        
        # По ТЗ: Курс валюты неверный тип → TypeError
        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(value)}")
        
        result[code] = value
    
    return result


# ==========================================
# ЛОГИРОВАНИЕ
# ============================================

# создать логгер logging.getLogger("currency")"
file_logger = logging.getLogger("currency")  
file_logger.setLevel(logging.INFO)

# Настраиваем запись в файл
file_handler = logging.FileHandler('currency.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Формат сообщений
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик
file_logger.addHandler(file_handler)

# Вывод в консоль для отладки 
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
# file_logger.addHandler(console_handler)

# Вариант 1: В файл (по ТЗ)
@logger(handle=file_logger)
def get_currencies_file(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """Версия с файловым логированием"""
    return get_currencies(currency_codes, url)

# Вариант 2: В консоль (по умолчанию)
@logger
def get_currencies_console(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """Версия с логированием в консоль"""
    return get_currencies(currency_codes, url)


# # Пример использования функции:
# currency_list = ['AED', 'AUD', 'UAH', 'USD', 'EUR', 'GBP']

# currency_data = get_currencies_file(currency_list, url='https://www.cbr-xml-daily.ru/daily_json.js')
# currency_data = get_currencies_console(currency_list, url='https://www.cbr-xml-daily.ru/daily_json.js')


if __name__ == "__main__":
    print("=" * 60)
    print("Демонстрация работы программы")
    print("=" * 60)
    
    currency_list = ['AED', 'AUD', 'UAH', 'USD', 'EUR', 'GBP']
    
    print("\n1. Получение курсов валют с файловым логированием:")
    try:
        result = get_currencies_file(currency_list)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    print("\n2. Получение курсов валют с консольным логированием:")
    try:
        result = get_currencies_console(currency_list)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    print("\n3. Демонстрация квадратного уравнения:")
    test_cases = [
        ("Два корня (INFO)", (1, -3, 2)),
        ("Один корень (INFO)", (1, 2, 1)),
        ("Отрицательный дискриминант (WARNING)", (1, 1, 1)),
        ("Некорректные данные (ERROR)", ("abc", 2, 3)),
        ("Вырожденное уравнение (CRITICAL)", (0, 0, 5)),
    ]
    
    for name, (a, b, c) in test_cases:
        print(f"\n   {name}: a={a}, b={b}, c={c}")
        try:
            result = solve_quadratic(a, b, c)
            print(f"      Корни: {result}")
        except Exception as e:
            print(f"      Ошибка: {e}")
    
    print("\n" + "=" * 60)
    print("Демонстрация завершена. Проверьте файл currency.log")
    print("=" * 60)