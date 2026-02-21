from typing import Callable 
import matplotlib.pyplot as plt
from typing import Callable, Dict, Any
from collections import deque
from trees import build_tree_recursive, build_tree_iterative
import timeit


# Уникальное дерево №15 - Root = 15; height = 6, left_leaf = 2*(root+1), right_leaf = 2*(root-1)
def main() -> None:
    """

    """

    # Основные переменные
    root = 15
    height = 6


    # ввод формул правой и левой ветки
    #l_b = lambda x : 2*(x+1)
    #r_b = lambda x : 2*(x-1)
    
    #output_bin_tree(build_tree_iterative())
    
    
    test_data1 = list(range(1, 10))
    
    build_plot(test_data1, build_tree_recursive, build_tree_iterative)

    

def build_plot(test_data: list[int]=list(range(10, 300, 10)), tree_1: Callable=build_tree_recursive, tree_2: Callable=build_tree_iterative) -> None:

    """
    Документация функции
    """
    
    res_1 = []
    res_2 = []

    # Вычисление производительности функций
    for n in test_data:
      res_1.append(benchmark(tree_1, n))
      res_2.append(benchmark(tree_2, n))


    # Визуализация
    plt.plot(test_data, res_1, label="Рекурсивное дерево")
    plt.plot(test_data, res_2, label="Итеративное дерево")
    plt.title("Сравнение рекурсивного и итеративного деревьев")


    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.legend()    
    plt.show()



def benchmark(func: Callable, n: int, number: int=1, repeat: int=5) -> int:
    """Возвращает среднее время выполнения func(n)"""
    def setup():
        """Функция setup для timeit - очищает кеш перед каждым повторением"""
        if hasattr(func, 'cache_clear'):
            func.cache_clear()


    times = timeit.repeat(lambda: func(n), setup=setup, number=number, repeat=repeat)
    return min(times)





if __name__ == '__main__':
    main()










