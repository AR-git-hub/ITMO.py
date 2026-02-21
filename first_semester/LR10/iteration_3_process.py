import doctest
import math
from multiprocessing import Process
from typing import Callable
from iteration_1_basic_integral import integrate
from benchmark import benchmark
from functools import partial


# итерация 2
# оптимизация с помощью потоков

# итерация 3
# оптимизация с помощью процессов



def integrate_process(f: Callable, a: int, b: int, *, n_jobs: int=2, n_iter: int=100000) -> int:
    """Вычисляет интеграл с помощью процессов
    
    Приближенные вычисления осуществляются интегрированием методом левых прямоугольников. 
    Интегрируемые части отрезка разделяются на сферы влияния каждого процесса
    
    Args:
        f (Callable): математическая функция
        a (int): координата начала промежутка интегрирования по оси абцисс
        b (int): координата конца промежутка интегрирования по оси абцисс
        n_jobs (int): количество процессов (ограниченно числом ядер процессора)
        n_iter (int): кол-во итераций (прямоугольников)
    
    Returns:
        int: интеграл (площадь под графиком данной функции)
        
    Examples:
    >>>
    
    """
    
    step = (b - a) / n_jobs
    
    # spawn = partial(integrate, f, n_iter=(n_iter//n_jobs))
    
    prcs = [Process(target=integrate, args=(f, (a + i*step), (a + (i+1)*step) ), kwargs=(n_iter:=n_iter//n_jobs), daemon=True) for i in range (n_jobs)]
    # for i in range(n_jobs):   
        # print(f"i: {i}, step: {step}, a: {a}.\n(a + step*i) = {a+step*i}, (a + step*(i+1)) = {a+step*(i+1)}, b: {b}")
    
    res = 0
    for p in prcs:
        p.start()
        p.join()
        print(p, type(p))
        
    return res
    
    
    
    
if __name__ == "__main__":
    # doctest.modtest(verbose=True)
    print('GG')
    
    print(integrate_process(math.sin, 0, math.pi))
    print('GG')
    # benchmark(integrate, math.sin, 0, math.pi)
    # benchmark(integrate_process, math.sin, 0, math.pi)




