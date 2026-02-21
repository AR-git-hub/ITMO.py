import timeit
import doctest
import statistics
from typing import Callable, Any


def benchmark(f: Callable[[], Any], *args: Any, **kwargs: Any) -> None:
    """Универсальный бенчмарк
    
    Выводит результат измерения времени выполнения функции при разных значениях количества итераций
    
    Args: 
    f (Callable): Функция, для которой производится измерение времени выполнения
    *args (Any): позиционные аргументы для f
    **kwargs (Any): ключевые аргументы для f
    
    Notes:
    Вызывать функцию можно так.
    
    Вызов. 
    benchmark(lambda x:x**1000-3*x**900)
    
    Вывод. 
    При количестве итераций: «10» время, за которое функция завершает свою работу: «Х»
    При количестве итераций: «100» время, за которое функция завершает свою работу: «Х»
    При количестве итераций: «1000» время, за которое функция завершает свою работу: «Х»
    При количестве итераций: «10000» время, за которое функция завершает свою работу: «Х»
    При количестве итераций: «100000» время, за которое функция завершает свою работу: «Х»
    """
    
    till = 2 # порядок повторовений вызова функции (10^2, 10^3...)
    iterations = [10**n for n in range(1, till+1)]
    test_func = lambda: f(*args, **kwargs)
    
    print("\n========================================")
    for n_iter in iterations:
        res = timeit.repeat(test_func, repeat=5, number=n_iter)
        t = statistics.median(res)
        # t = timeit.timeit(test_func, number=n_iter)
        print(f"При количестве итераций: «{n_iter}» медианное время, за которое функция «{f.__name__}» завершает свою работу: «{t}» секунд")
    print("========================================")   
    

def test_factorial(n: int) -> int:
    """Считает значение факториала числа
    
    Подсчеты выполняются итерационным методом
    
    Args:
    n (int): Исходное число, для которого считаем факториал
    
    Returns:
    int: Результат вычисления факториала
    
    Raises:
    ValueError: Если на вход подано не натуральное число
    
    Examples:
    >>> test_factorial(5)
    120
    """
    
    res = 1
    for i in range(1, n+1):
        res *= i
        
    return res


if __name__ == '__main__':
    #doctest.testmod(verbose=True)
    
    benchmark(test_factorial, 100)
