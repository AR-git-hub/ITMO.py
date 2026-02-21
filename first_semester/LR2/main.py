from typing import Callable 


# Уникальное дерево №15 - Root = 15; height = 6, left_leaf = 2*(root+1), right_leaf = 2*(root-1)
def main() -> None:
    """
    Программа для рассчета бинарного дерева, исходя из заданных условий (корень и формулы веток)
    Для того, чтобы проверить работоспособность функции можно менять 
    root - корень дерева
    height - глубина дерева

    l_b, r_b - формулы задачи левой и правой веток соответственно
    
    """

    global tree, spaces, l_b, r_b

    
    # Основные переменные
    root = 15
    height = 6

    # tree - двумерный массив, для красивого вывода дерева
    tree = [[] for i in range(height+1)]
    tree[0] = [str(root)]
    
    # ввод формул правой и левой ветки
    l_b = lambda x : 2*(x+1)
    r_b = lambda x : 2*(x-1)
    
    print(gen_bin_tree(height, root))
    # раскомментировать следующую строчку и закомментировать данную, а также в gen_bin_tree return изменить на tree для того, чтобы увидеть красивый вывод
    #output_bin_tree(gen_bin_tree(height,root), spaces=90)

    
def left_branch(root: int) -> int:
    global l_b, r_b

    if l_b(3)==8 and r_b(3)==4:
        return l_b(root)
    else:
        return l_b(root)

def right_branch(root: int) -> int:
    global l_b, r_b

    if l_b(3)==8 and r_b(3)==4:
        return r_b(root)
    else:
        return r_b(root)


def gen_bin_tree(height: int = 6 , root: int = 15, h: int = 1) -> dict[int:int] | list[list[str]]:
    """
    Генерирует бинарное дерево в виде словаря.

    Каждый узел: {значение: {'left': левое_поддерево, 'right': правое_поддерево}}
    Листья: {значение: {}}
    """
    
    global tree
    
    if height > 1:

        # добавляем ветку двумерный массив tree
        tree[h].append(str(get_left_branch(height, root, h, flag=True)))
        tree[h].append(str(get_right_branch(height, root, h, flag=True)))
        
        
        # добавляем ветку в словарь-дерево d
        d = {root: [get_left_branch(height, root, h), get_right_branch(height, root, h)]}
        
        return d # изменить на tree для красивого вывода
    else:
        return 0


def get_left_branch(height: int, root: int, h: int, flag: bool = False) -> Callable[[int, int, int], dict[int:dict[int: int]] | list[list[str]]]:
    """
    Генерирует левую ветку дерева.
    """

    # блок кода для красивого вывода при flag = true, иначе - стандартное выполнение
    if flag:
        h += 1
        return left_branch(root)
    
    return gen_bin_tree(height-1, left_branch(root), h+1)


def get_right_branch(height: int, root: int, h: int, flag: bool = False) -> Callable[[int, int, int], dict[int:dict[int: int]] | list[list[str]]]:
    """
    Генерирует правую ветку дерева.
    """

    # блок кода для красивого вывода при flag = true, иначе - стандартное выполнение
    if flag:
        h += 1
        return right_branch(root)
    
    return gen_bin_tree(height-1, right_branch(root), h+1)


def output_bin_tree(tree: list[list[str]], spaces: int = 128) -> None:

    """
    Красивый вывод дерева (списка tree), опираясь на математическую модель
    spaces - базовый межстрочный интервал (рекомендуется использовать в пределах 70-150)
    Ничего не возвращает
    """

    # рассчет расстояния между числами
    interval_count = {'0': spaces//2, '1': spaces//4, '2':spaces//8, '3':spaces//16, '4':spaces//32, '5':spaces//64, '6':spaces//128}

    
    # вывод чисел
    print()
    for i in range(len(tree)-1):
        print(str(i+1)+'й уровень: '+' '*10, end='')       
    
        interval = interval_count.get(str(i))
        
        
        for j in range(len(tree[i])):          
            
            print(interval*'_' + str(tree[i][j]) + interval*'_', end='')
            

        print(end='\n\n')
        
        


if __name__ == '__main__':
    main()










