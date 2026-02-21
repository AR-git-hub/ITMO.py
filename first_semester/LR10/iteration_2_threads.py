import concurrent.futures as ftres
import doctest
import threading
import math
from functools import partial
from typing import Callable
from iteration_1_basic_integral import integrate
from benchmark import benchmark


# итерация 2
# оптимизация с помощью потоков

# итерация 3
# оптимизация с помощью процессов



def integrate_threads(f: Callable, a: int, b: int, *, n_jobs: int=2, n_iter: int=100000) -> int:
    """Вычисляет интеграл с помощью потоков
    
    Приближенные вычисления осуществляются интегрированием методом левых прямоугольников. 
    Интегрируемые части отрезка разделяются на сферы влияния каждого потока
    
    Args:
        f (Callable): математическая функция
        a (int): координата начала промежутка интегрирования по оси абцисс
        b (int): координата конца промежутка интегрирования по оси абцисс
        n_jobs (int): количество потоков
        n_iter (int): кол-во итераций (прямоугольников)
    
    Returns:
        int: интеграл (площадь под графиком данной функции)
        
    Examples:
    >>>
    
    """
    
    
    #   - реализовать аналогичную функцию для вычисления с процессами (ProcessPoolExecutor)
    #   - оценить время работы программ с потоками и процессами и зафиксировать значения (2, 4, 6, 8(?))
   

    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs) # создаваемый пул тредов будет размера n_jobs

    spawn = partial(executor.submit, integrate, f, n_iter = n_iter // n_jobs)   # partial позволяет "закрепить"
                                                                                # несколько аргументов
                                                                                # для удобства вызова функции ,
                                                                                # см. пример ниже
    step = (b - a) / n_jobs
    # for i in range(n_jobs):
    #   print(f"Работник {i}, границы: {a + i * step}, {a + (i + 1) * step}")

    threads = [spawn((a + i*step), (a + (i+1)*step)) for i in range(n_jobs)]    # создаем потоки с помощью генератора
                                                                             # списков; partial позволил нам

    return sum(list(thread.result() for thread in ftres.as_completed(threads)))                     # as.completed() берет на вход список
                                                                                # фьючерсов и как только какой-то
                                                                                # завершился, возвращает результат
                                                                                # f.result(), далее, мы эти результаты
                                                                                # складываем

if __name__ == "__main__":
    # doctest.modtest(verbose=True)
    # print(integrate_threads(math.sin, 0, math.pi))
    benchmark(integrate, math.sin, 0, math.pi)
    benchmark(integrate_threads, math.sin, 0, math.pi)




