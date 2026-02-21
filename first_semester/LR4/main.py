import timeit
import matplotlib.pyplot as plt
from typing import Callable
from factorials import *


def benchmark(func: Callable, n: int, number: int=1, repeat: int=5) -> int:
    """Возвращает среднее время выполнения func(n)"""
    def setup():
        """Функция setup для timeit - очищает кеш перед каждым повторением"""
        if hasattr(func, 'cache_clear'):
            func.cache_clear()


    times = timeit.repeat(lambda: func(n), setup=setup, number=number, repeat=repeat)
    return min(times)


def build_plot(test_data: list[int]=list(range(10, 300, 10)), fact_1: Callable[[int], int]=fact_recursive, fact_2: Callable[[int], int]=fact_iterative) -> None:

    """
    Документация функции
    """

    # список функций факториалов для дальнейшего сравнения со всевозможными
    d = [fact_1, fact_2]


    # возможные комбинации ввода: Р+И, РК+ИК, Р+РК, И+ИК, Р+ИК, РК+И - 6 вариантов + 6 НАОБОРОТ
    # Р+И,  И+Р
    d_rec_iterative = [fact_recursive, fact_iterative]

    # РК+И, ИК+Р
    d_reccache_iterativecache = [fact_recursive_cache, fact_iterative_cache]

    # Р+РК, РК+Р
    d_rec_reccache = [fact_recursive, fact_recursive_cache]

    # И+ИК, ИК+И
    d_iterative_iterativeccache = [fact_iterative, fact_iterative_cache]

    # РК+И, И+РК
    d_reccache_iterative = [fact_recursive_cache, fact_iterative]

    # Р+ИК, ИК+Р
    d_rec_iterativecache = [fact_recursive, fact_iterative_cache]

    
    if d not in [d_rec_iterative, d_reccache_iterativecache, d_rec_reccache, d_iterative_iterativeccache, d_reccache_iterative, d_rec_iterativecache, d_rec_iterative[::-1],d_reccache_iterativecache[::-1], d_rec_reccache[::-1], d_iterative_iterativeccache[::-1], d_reccache_iterative[::-1], d_rec_iterativecache[::-1]]:
        raise Exception("Введены функции не из списка: (кэшированные) итеративный и рекурсивный факториал")

    res_1 = []
    res_2 = []

    # Вычисление производительности функций
    for n in test_data:
      res_1.append(benchmark(fact_1, n))
      res_2.append(benchmark(fact_2, n))


    # Визуализация

    # Р+И, И+Р
    if d==d_rec_iterative:
        plt.plot(test_data, res_1, label="Рекурсивный")
        plt.plot(test_data, res_2, label="Итеративный")
        plt.title("Сравнение рекурсивного и итеративного факториала")

    if d==d_rec_iterative[::-1]:
        plt.plot(test_data, res_1, label="Итеративный")
        plt.plot(test_data, res_2, label="Рекурсивный")
        plt.title("Сравнение итеративного и рекурсивного факториала")


    # РК+ИК, ИК+РК
    if d==d_reccache_iterativecache:
        plt.plot(test_data, res_1, label="Рекурсивный кэшированный")
        plt.plot(test_data, res_2, label="Итеративный кэшированный")
        plt.title("Сравнение кэшированных рекурсивного и итеративного факториала")

    if d==d_reccache_iterativecache[::-1]:
        plt.plot(test_data, res_1, label="Итеративный кэшированный")
        plt.plot(test_data, res_2, label="Рекурсивный кэшированный")
        plt.title("Сравнение кэшированных итеративного и рекурсивного факториала")
        
    
    # Р+РК, РК+Р
    if d==d_rec_reccache:
        plt.plot(test_data, res_1, label="Рекурсивный")
        plt.plot(test_data, res_2, label="Рекурсивный кэшированный")
        plt.title("Сравнение рекурсивного и кэшированного рекурсивного факториала")

    if d==d_rec_reccache[::-1]:
        plt.plot(test_data, res_1, label="Рекурсивный кэшированный")
        plt.plot(test_data, res_2, label="Рекурсивный")
        plt.title("Сравнение кэшированного рекурсивного и рекурсивного факториала")
        

    # И+ИК, ИК+И
    if d==d_iterative_iterativeccache:
        plt.plot(test_data, res_1, label="Итеративный")
        plt.plot(test_data, res_2, label="Итеративный кэшированный")
        plt.title("Сравнение итеративного и кэшированного итеративного факториала")

    if d==d_iterative_iterativeccache[::-1]:
        plt.plot(test_data, res_1, label="Итеративный")
        plt.plot(test_data, res_2, label="Рекурсивный")
        plt.title("Сравнение кэшированного итеративного и итеративного факториала")
        
    
    # РК+И, И+РК
    if d==d_reccache_iterative:
        plt.plot(test_data, res_1, label="Рекурсивный кэшированный")
        plt.plot(test_data, res_2, label="Итеративный")
        plt.title("Сравнение кэшированного рекурсивного и итеративного факториала")

    if d==d_reccache_iterative[::-1]:
        plt.plot(test_data, res_1, label="Итеративный")
        plt.plot(test_data, res_2, label="Рекурсивный кэшированный")
        plt.title("Сравнение итеративного и кэшированного рекурсивного факториала")

    # Р+ИК, ИК+Р
    if d==d_rec_iterativecache:
        plt.plot(test_data, res_1, label="Рекурсивный")
        plt.plot(test_data, res_2, label="Итеративный кэшированный")
        plt.title("Сравнение рекурсивного и кэшированного итеративного факториала")

    if d==d_rec_iterativecache[::-1]:
        plt.plot(test_data, res_1, label="Итеративный")
        plt.plot(test_data, res_2, label="Рекурсивный кэшированный")
        plt.title("Сравнение кэшированного итеративного и рекурсивного факториала")


    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.legend()    
    plt.show()



def main():
    # фиксированные наборы данных
    #test_data1 = list(range(10, 300, 10))
    test_data1 = list(range(10, 900, 10))

    #build_plot(test_data1, lambda x: x+1, fact_recursive) # "вызов" ошибки
    
    # ВСЕ ВАРИАНТЫ ДЛЯ ТЕСТА
    build_plot(test_data1, fact_iterative, fact_recursive)
    build_plot(test_data1, fact_recursive, fact_iterative)
    
    build_plot(test_data1, fact_iterative_cache, fact_recursive_cache)
    build_plot(test_data1, fact_recursive_cache, fact_iterative_cache)


    build_plot(test_data1, fact_iterative_cache, fact_recursive)
    build_plot(test_data1, fact_recursive, fact_iterative_cache)


    build_plot(test_data1, fact_iterative, fact_recursive_cache)
    build_plot(test_data1, fact_recursive_cache, fact_iterative)


    build_plot(test_data1, fact_iterative_cache, fact_iterative)
    build_plot(test_data1, fact_iterative, fact_iterative_cache)


    build_plot(test_data1, fact_recursive, fact_recursive_cache)
    build_plot(test_data1, fact_recursive_cache, fact_recursive)
    
    


if __name__ == "__main__":
    main()

# import timeit


# print('Не меморизованная (мс): ', min(timeit.repeat("factorial(100)", setup="def factorial(n):\n\treturn n * factorial(n-1) if n else 1;", repeat=5, number=1000))*1000)

# print('Меморизованная (мс) : ', min(timeit.repeat("factorial(100)", setup="from functools import lru_cache;\n@lru_cache\ndef factorial(n):\n\treturn n * factorial(n-1) if n else 1;", repeat=5, number=1000))*1000)