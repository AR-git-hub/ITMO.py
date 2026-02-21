from typing import Callable


def main() -> None:
    """
    Ввод значений с клавиатуры для формирования
    списка, по которому мы ищем искомое число и
    искомого числа
    (опционально) предложить пользователю сформировать
    список вручную с клавиатуры

    __вызов функции guess-number с параметрами: __
      - искомое число (target)
      - список, по-которому идем
      - тип поиска (последовательный, бинарный)

    __вывод результатов на экран__
    :return:
    """

    # Создаем базовые переменные. При плохом вводе - ловим ошибку
    try: 
        target = int(input('Введите target : '))
    except ValueError:
        raise ValueError('Некорректное значение target')

    try: 
        start_range = int(input('Введите начало диапазона : '))
    except ValueError:
        raise ValueError('Некорректное значение начала диапазона')
    
    try: 
        end_range = int(input('Введите конец диапазона : '))
    except ValueError:
        raise ValueError('Некорректное значение конца диапазона')
    
    
    if start_range > end_range:
        raise Exception('Начало дипазона больше его конца')
    
    # Автоматически создаем список
    d = list(range(start_range, end_range + 1))
    

    # Создание списка вручную
    # d = helper()

    # Проверяем, входит ли target в список
    if target not in d:
        raise Exception('target не входит в данный числовой ряд')

    # выводим результат
    res = guess_number(target, d, type='bin')
    print(f'{res}')


def guess_number(target: int, lst: list[int], type: str = 'seq') -> list[int, int | None]:

    """
    Функция для нахождения искомого числа по заданным алгоритмам:
    seq - медленный инкрементальный поиск
    bin - бинарный алгоритм поиска

    возвращает список из найденного числа и затраченного количества попыток
    
    """
    
    if type == 'seq':
        tries = 1
        for i in range(len(lst)):     
            if lst[i] == target:
                break

            tries += 1
        res = lst[i]
        
    
    elif type == 'bin':
        tries = 1

        r =  len(lst)-1 # правый крайний индекс
        l = 0 # левый крайний индекс
        middle = r//2

        while lst[middle] != target:
            #print('left: ', l, ', right: ', r, ', middle: ', middle, ', list:', lst[l:r+1], sep='' )
            
            tries += 1
            #print('left: ', l, ', right: ', r, ', middle: ', middle, ', list:', lst[l:r+1], sep='' )
                        
            if lst[middle]>target:
                r = middle - 1
            else:
                l = middle + 1

            middle = l + (r-l)//2
            
        res = lst[middle]

    else:
        raise Exception('Некорректное значение type')


    return [res, tries]


def helper() -> list[int]:
    """
    Функция для ручного ввода списка.

    Возвращает поданный на вход список.
    """

    enter_lst = input('Введите значения списка через пробел : ')  

    # Проверка ввел ли пользователь список из чисел, пробелов и знака минус
    for el in enter_lst:
        if el not in '-0123456789 ':
            raise Exception('Введены некорректные символы')
        

    # Проверяем, если есть отрицательные числа, правильно ли они написаны
    # пусть правильно только так : '-2 -3 53 -4'
    enter_lst_copy = enter_lst[:]
    for i in '0123456789':
        enter_lst_copy.replace(i,'1')
    if '- 1' in enter_lst_copy or '1- ' in enter_lst_copy or '--' in enter_lst_copy or ' - ' in enter_lst_copy or '1-1' in enter_lst_copy:
        raise Exception('Некорректный ввод отрицательных чисел')


    return sorted(list(map(int, enter_lst.split())))


if __name__ == '__main__':
    main()
