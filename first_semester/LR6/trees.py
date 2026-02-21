from typing import Callable, Dict, Any
from collections import deque


def build_tree_recursive(height: int=6, root: int=15, l_b: Callable[[int], int]=lambda x: 2*(x+1), r_b: Callable[[int], int]=lambda x: 2*(x-1), h: int=0) -> Dict[str, str | Any]:
    
    if h==height-1:
        return {str(root): []}
    left_child = build_tree_recursive(height, l_b(root), l_b, r_b, h+1)
    right_child = build_tree_recursive(height, r_b(root), l_b, r_b, h+1)
    
    return {str(root): [left_child, right_child]}


def build_tree_iterative(height: int=6, root: int=15, l_b: Callable[[int], int]=lambda x: 2*(x+1), r_b: Callable[[int], int]=lambda x: 2*(x-1)) -> Dict[str, str | Any]:
    
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
             