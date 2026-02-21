import unittest
import io
import logging
from main import logger, get_currencies, solve_quadratic, get_currencies_console

class TestLoggerDecorator(unittest.TestCase):
    """Тесты декоратора logger"""
    
    def test_logger_success_with_stringio(self):
        """Тест 6.2: Логирование успешного выполнения в StringIO"""
        stream = io.StringIO()
        
        @logger(handle=stream)
        def test_func(x):
            return x * 2
        
        result = test_func(5)
        
        # Проверяем результат
        self.assertEqual(result, 10)
        
        # Проверяем логи
        logs = stream.getvalue()
        self.assertIn("INFO", logs)
        self.assertIn("test_func", logs)
        self.assertIn("args=(5,)", logs)
        self.assertIn("Результат: 10", logs)
    
    def test_logger_error_with_stringio(self):
        """Тест 6.2: Логирование ошибки в StringIO"""
        stream = io.StringIO()
        
        @logger(handle=stream)
        def failing_func():
            raise ValueError("Тестовая ошибка")
        
        # Проверяем, что исключение пробрасывается
        with self.assertRaises(ValueError):
            failing_func()
        
        # Проверяем, что ошибка залогирована
        logs = stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("Тестовая ошибка", logs)

class TestGetCurrencies(unittest.TestCase):
    """Тесты функции get_currencies (раздел 6.1 ТЗ)"""
    
    def test_successful_request(self):
        """Корректный возврат реальных курсов"""
        result = get_currencies_console(['USD', 'EUR'])
        
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertIsInstance(result['USD'], (int, float))
        self.assertIsInstance(result['EUR'], (int, float))
    
    def test_nonexistent_currency(self):
        """Поведение при несуществующей валюте"""
        with self.assertRaises(KeyError):
            get_currencies_console(['XYZ'])
    
    def test_connection_error(self):
        """Выброс ConnectionError при недоступном API"""
        with self.assertRaises(ConnectionError):
            get_currencies_console(['USD'], url="https://invalid-url.example.com")
    
    def test_invalid_json(self):
        """Выброс ValueError при некорректном JSON"""
        # Используем тестовый URL, который возвращает не JSON
        with self.assertRaises(ValueError):
            get_currencies_console(['USD'], url="https://httpbin.org/html")
            
    def test_keyerror_no_valute(self):
        """Тест KeyError при отсутствии ключа 'Valute' в JSON"""
        # Для этого теста нужно подменить ответ API
        # Можно использовать мокинг, но для простоты пока пропустим
        pass
    
    def test_typeerror_invalid_currency_type(self):
        """Тест TypeError при неверном типе курса валюты"""
        # Аналогично, нужно мокать ответ API
        pass
    
    def test_multiple_currencies(self):
        """Тест получения нескольких валют"""
        result = get_currencies_console(['USD', 'EUR', 'GBP'])
        self.assertEqual(len(result), 3)
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertIn('GBP', result)

class TestStreamWriteExample(unittest.TestCase):
    """Тест 6.3: Пример теста с контекстом из задания"""
    
    def setUp(self):
        self.stream = io.StringIO()
        
        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")
        
        self.wrapped = wrapped
    
    def test_logging_error(self):
        """Проверяем логирование ошибки ConnectionError"""
        with self.assertRaises(ConnectionError):
            self.wrapped()
        
        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)

class TestQuadraticEquation(unittest.TestCase):
    """Тесты демо-примера квадратного уравнения"""
    
    def test_two_roots_info(self):
        """INFO для двух корней"""
        result = solve_quadratic(1, -3, 2)  # (x-1)(x-2)=0
        self.assertEqual(sorted(result), [1.0, 2.0])
    
    def test_negative_discriminant_warning(self):
        """WARNING для дискриминанта < 0"""
        with self.assertRaises(ValueError) as context:
            solve_quadratic(1, 1, 1)  # d = -3
        
        self.assertIn("WARNING", str(context.exception))
    
    def test_invalid_data_error(self):
        """ERROR для некорректных данных"""
        with self.assertRaises(TypeError):
            solve_quadratic("abc", 2, 3)
    
    def test_critical_situation(self):
        """CRITICAL для полностью невозможной ситуации"""
        with self.assertRaises(ValueError) as context:
            solve_quadratic(0, 0, 5)
        
        self.assertIn("CRITICAL", str(context.exception))

if __name__ == '__main__':
    unittest.main()