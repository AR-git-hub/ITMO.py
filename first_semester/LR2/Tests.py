import unittest
from guess_number import guess_number
from guess_number import main


# Тесты
class TestMath(unittest.TestCase):

    
    ### Тесты над main()
    ## Плохие типы (либо неправильно введенные отрицательные числа)
    # Плохой тип target
    def test_bad_type_target(self):
        print('\nТест на тип target. В поле target введите не int')
        with self.assertRaises(ValueError) as ctx:
            main()

        self.assertTrue('Некорректное значение target' in str(ctx.exception))


    # Плохой тип start
    def test_bad_type_start(self):
        print('\nТест на тип start. В поле начало диапазона введите не int')
        with self.assertRaises(ValueError) as ctx:
            main()

        self.assertTrue('Некорректное значение начала диапазона' in str(ctx.exception))


    # Плохой тип end
    def test_bad_type_end(self):
        print('\nТест на тип end. В поле конец диапазона введите не int')
        with self.assertRaises(ValueError) as ctx:
            main()

        self.assertTrue('Некорректное значение конца диапазона' in str(ctx.exception))


    ## Плохой диапазон или target
    # Если начало диап больше конца
    def test_start_greater_than_end(self):
        print('\nstart > end ? В поле начало диапазона введите значение, больше чем в поле конец')
        with self.assertRaises(Exception) as ctx:
            main()

        self.assertTrue('Начало дипазона больше его конца' in str(ctx.exception))


    # target не входит в диапазон
    def test_target_not_in_range(self):
        print('\nЧисло не входит в диапазон. Введите диапазон такой, что target будет лежать вне его')
        with self.assertRaises(Exception) as ctx:
            main()

        self.assertTrue('target не входит в данный числовой ряд' in str(ctx.exception))


    ## Может ли программа принять на вход отрицательные числа?
    def test_target_not_in_range(self):
        print('\nОтрицательные числа. Попробуйте ввести отрицательные target, начало и конец диапазона (соблюдая остальные правила)')
        with self.assertRaises(Exception) as ctx:
            main()

        self.assertTrue('' in str(ctx.exception))


    ### Тесты над guess_number()
    ## Тесты с seq
    
    ## Правильные случаи
    def test_normal_input_seq_1(self):
        self.assertEqual(guess_number(3, [1,2,3,4,5]), [3, 3])


    def test_normal_input_seq_2(self):
        self.assertEqual(guess_number(5, [0,1,2,3,4,5]), [5, 6])
    

    # Отрицательные числа
    def test_negative_target_seq_1(self):
        self.assertEqual(guess_number(-3, [-5,-4,-3,-2,-1]), [-3, 3])


    def test_negative_target_seq_2(self):
        self.assertEqual(guess_number(-3, [-5,-4,-3,-2,-1,0,1,2]), [-3, 3])


    def test_negative_target_seq_3(self):
        self.assertEqual(guess_number(3, [-5,-4,-3,-2,-1,0,1,2,3,4,5]), [3, 9])

    
    ## Тесты с bin
    # Правильный случай
    def test_normal_input_bin_1(self):
        self.assertEqual(guess_number(4, [1,2,3,4,5], 'bin'), [4, 2])


    def test_normal_input_bin_2(self):
        self.assertEqual(guess_number(5, [0,1,2,3,4,5], 'bin'), [5, 3])


    # Отрицательные числа
    def test_negative_target_bin_1(self):
        self.assertEqual(guess_number(-3, [-5,-4,-3,-2,-1], 'bin'), [-3, 1])


    def test_negative_target_bin_2(self):
        self.assertEqual(guess_number(-1, [-5,-4,-3,-2,-1,0,1,2], 'bin'), [-1, 3])


    def test_negative_target_bin_3(self):
        self.assertEqual(guess_number(3, [-5,-4,-3,-2,-1,0,1,2,3,4,5], 'bin'), [3, 2])


    """
    ### Тесты со списком, введенным от руки
    # Состоит ли список (введенный от руки) из чего-либо помимо чисел (отрицательных и положительных) и пробелов
    def test_input_list_not_int(self):
        print('\nНеккоректные значения списка. Введите в список что-либо помимо чисел (отрицательных и положительных) и пробелов')
        with self.assertRaises(Exception) as ctx:
            main()

        self.assertTrue('Введены некорректные символы' in str(ctx.exception))
    

    # Некорректный ввод отрицательных чисел: '- 1', ' - ', '1- ', '1-1', '--'
    def test_negative_incorrect_inputlist(self):
        print('\nНекорректный ввод отрицательных чисел в список. Введите такой список, что в нем будут примеры чисел выше ("- 1", " - ", "1- ", "1-1", "--")')
        with self.assertRaises(Exception) as ctx:
            main()

        self.assertTrue('Некорректный ввод отрицательных чисел' in str(ctx.exception))

    
    # target нет в значениях списка
    def test_target_not_in_inputlist(self):
        print('\nЧисло не входит в список. Введите такой список, что target не будет его значением')
        with self.assertRaises(Exception) as ctx:
            main()

        self.assertTrue('target не входит в данный числовой ряд' in str(ctx.exception))
    

    ## Правильные случаи

    # Список не отсортированный
    def test_not_sorted_inputlist(self):
        self.assertEqual(guess_number(3, [2,4,3,0,1], 'seq'), [3, 3])


    # Список содержит отрицательные числа
    def test_negative_list_inputlist(self):
        self.assertEqual(guess_number(3, [-2,-4,3,-0,1], 'seq'), [3, 3])


    # Target - отрицательное число
    def test_negative_target_inputlist(self):
        self.assertEqual(guess_number(-3, [2,4,-3,0,1], 'seq'), [-3, 3])


    # Список содержит повторящиеся числа
    def test_repetetive_numbers_inputlist(self):
        self.assertEqual(guess_number(-3, [2,2,3,3,-3,-3,5,1], 'seq'), [-3, 5])   
    
    """



# Запуск тестов
if __name__ == '__main__':
    unittest.main()
    




