import math
import timeit
import doctest
from typing import Callable
from multiprocessing import Process
from benchmark import benchmark


# А ТАКЖЕ ДОКУМЕНТАЦИЮ ДЛЯ КАЖДОГО МОДУЛЯ!!!!
# чем являются объекты списка fs - вопрос на понимание кода ЛР9


# итерация 1
def integrate(f:Callable, a: int | float, b: int | float, *, n_iter: int=100000) -> int | float:
  """Вычисляет интеграл.
  
  Приближенные вычисления осуществляются интегрированием методом левых прямоугольников

  Args:
    f (Callable): математическая функция, 
    a (int): координата начала промежутка интегрирования по оси абцисс
    b (int):  координата конца промежутка интегрирования по оси абцисс
    n_iter (int): количество итераций

  Returns:
    int: интеграл (площадь под графиком данной функции)
    
  Examples:
  >>> round(integrate(math.cos, 0, math.pi / 2, n_iter=100), 5)
  1.00783
  
  >>> round(integrate(lambda x: 4*x**2 - 3*x + 8.3, -2, 2, n_iter=100), 10)
  54.7776
  """
  
  
  # - замерить время вычисления функции (timeit), записать время
  # - + тесты с помощью Unittest / py.test
  
  acc = 0
  step = (b - a) / n_iter
  for i in range(n_iter):
    acc += f(a + i*step) * step
  return acc

# integrate(math.cos, 0, math.pi, n_iter=100)

# print(integrate(math.sin, 0, 100))
if __name__ == "__main__":
  doctest.testmod(verbose=True)
  benchmark(integrate, math.sin, - math.pi / 2, math.pi / 2, n_iter=100)
  




# def fetch_data(api_url, timeout=30, retry_count=3):

# """Fetches data from the specified API endpoint.

# This function handles retry logic and timeouts when
# communicating with external APIs.

# Args:
# api_url (str): The URL of the API endpoint.
# timeout (int, optional): Request timeout in seconds. Defaults to 30.
# retry_count (int, optional): Number of retry attempts. Defaults to 3.

# Returns:
# dict: The JSON response from the API as a dictionary.

# Raises:
# ConnectionError: If the API cannot be reached after retries.
# ValueError: If the response cannot be parsed as JSON.

# Examples:
# >>> data = fetch_data('https://api.example.com/data')
# >>> print(data['status'])
# 'success'
# """
