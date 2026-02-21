from typing import Callable, Dict, Any


# Уникальное дерево №15 - Root = 15; height = 6, left_leaf = 2*(root+1), right_leaf = 2*(root-1)
def main():
    """
    Программа для рассчета бинарного дерева, исходя из заданных условий (корень и формулы веток)
    Для того, чтобы проверить работоспособность функции можно менять 
    root - корень дерева
    height - глубина дерева

    """

    # Основные переменные
    #root = 15
    #height = 6

    # ввод формул правой и левой ветки
    # l_b = lambda x : 2*(x+1)
    # r_b = lambda x : 2*(x-1)
    
    #print(gen_bin_tree(height, root))
    # раскомментировать следующую строчку и закомментировать данную, а также в gen_bin_tree return изменить на tree для того, чтобы увидеть красивый вывод
    
    print(gen_bin_tree())
    #output_bin_tree() # красивый вывод


def gen_bin_tree(height: int=6, root: int=15, l_b: Callable[[int], int]=lambda x: 2*(x+1), r_b: Callable[[int], int]=lambda x: 2*(x-1), h: int=0) -> Dict[str, str | Any]:
    
    if h==height-1:
        return {str(root): []}
    left_child = gen_bin_tree(height, l_b(root), l_b, r_b, h+1)
    right_child = gen_bin_tree(height, r_b(root), l_b, r_b, h+1)
    
    return {str(root): [left_child, right_child]}
    

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










