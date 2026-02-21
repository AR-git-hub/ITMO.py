from functools import lru_cache
from typing import Callable


def fact_recursive(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


def fact_iterative(n: int) -> int:
    """Нерекурсивный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


@lru_cache(None)
def fact_recursive_cache(n: int) -> Callable[[int], int]:
    """Рекурсивный кэшированный факториал"""
    return fact_recursive(n) 


@lru_cache(None)
# разобраться с документацией
def fact_iterative_cache(n: int) -> Callable[[int], int]:
    """Нерекурсивный кэшированный факториал"""
    return fact_iterative(n)    
