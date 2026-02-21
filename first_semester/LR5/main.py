from typing import Callable, Dict, Any
from collections import deque


# Уникальное дерево №15 - Root = 15; height = 6, left_leaf = 2*(root+1), right_leaf = 2*(root-1)
def main() -> None:
    """
    Программа для рассчета бинарного дерева, исходя из заданных условий (корень и формулы веток)
    Для того, чтобы проверить работоспособность функции можно менять 
    root - корень дерева
    height - глубина дерева

    l_b, r_b - формулы задачи левой и правой веток соответственно
    
    """

    # Основные переменные
    root = 15
    height = 6

    # ввод формул правой и левой ветки
    #l_b = lambda x : 2*(x+1) 
    #r_b = lambda x : 2*(x-1)
    
    #output_bin_tree() # для красивого вывода
    print(gen_bin_tree(6, 15, lambda x: 3*(x+1), lambda x: 3*(x-1)))
    #output_bin_tree()
    

def gen_bin_tree(height: int=6, root: int=15, l_b: Callable[[int], int]=lambda x: 2*(x+1), r_b: Callable[[int], int]=lambda x: 2*(x-1)) -> Dict[str, str | Any]:
    
    tree = [[] for i in range(height)]
    tree[0] = [root]

    for h in range(1, height): 
        n = 2**(h) 
        # Кол-во элементов на ветке, четный эл - левая ветка, нечетный - правая
        anc = 0 # номер корня-предка для двух веток

        for i in range(0, n, 2):
            
            tree[h].append(l_b(tree[h-1][anc]))
            tree[h].append(r_b(tree[h-1][anc]))
            anc += 1
    
    
    # Строим дерево-словарь
    leaves = deque()
    
    for el in tree[-1]:
        leaves.append({str(el): []})
    
    for h in range(height-2, -1, -1):
        branch = deque()
        
        for el in tree[h]:
            left = leaves.popleft()
            right = leaves.popleft()
            
            branch.append({str(el): [left, right]})
        
        leaves = branch
        
    return leaves[0] # leaves - deque(); leaves[0] - Dict
             

def output_bin_tree(height: int=6, root: int=15, l_b: Callable[[int], int]=lambda x: 2*(x+1), r_b: Callable[[int], int]=lambda x: 2*(x-1), spaces: int = 128) -> None:

    """
    Красивый вывод дерева (списка tree), опираясь на математическую модель
    spaces - базовый межстрочный интервал (рекомендуется использовать в пределах 70-150)
    Ничего не возвращает
    """

    # Генерация для красивого вывода
    tree = [[] for i in range(height)]
    tree[0] = [root]

    for h in range(1, height): 
        n = 2**(h) 
        # Кол-во элементов на ветке, четный эл - левая ветка, нечетный - правая
        anc = 0 # номер корня-предка для двух веток

        for i in range(0, n, 2):
            
            tree[h].append(l_b(tree[h-1][anc]))
            tree[h].append(r_b(tree[h-1][anc]))
            anc += 1

    # рассчет расстояния между числами
    interval_count = {'0': spaces//2, '1': spaces//4, '2':spaces//8, '3':spaces//16, '4':spaces//32, '5':spaces//64, '6':spaces//128}

    
    # вывод чисел
    print()
    for i in range(len(tree)):
        print(str(i+1)+'й уровень: '+' '*10, end='')       
    
        interval = interval_count.get(str(i))
        
        
        for j in range(len(tree[i])):          
            
            print(interval*'_' + str(tree[i][j]) + interval*'_', end='')
            

        print(end='\n\n')
    
        


if __name__ == '__main__':
    main()










