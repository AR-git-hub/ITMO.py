import unittest
from main import two_sum


class TestTwoSum(unittest.TestCase):
  
  # Если список - None
  def test_nonetype(self):
    self.assertEqual(two_sum(None, 1), 'Список является значением класса NoneType')
  
  # Если "список" - не класс list
  def test_not_list(self):
    self.assertEqual(two_sum(2, 1), 'На вход подан не список')
    
  # Если список - пустой
  def test_empty_list(self):
    self.assertEqual(two_sum([],1), 'На вход подан пустой список')
  
  # Если в списке присутсвуют не int
  def test_not_int(self):
    self.assertEqual(two_sum([2,3.0],1), 'В списке присутсвуют не целые числовые значения') 
    
  # Если target - None
  def test_target_nonetype(self):
    self.assertEqual(two_sum([1,2], None), 'Переменна target является значением класса NoneType')
    
  # Если target - не int
  def test_target_not_int(self):
    self.assertEqual(two_sum([1,2], 'строка'), 'Переменна target не является целым числовым значением')
  
     
  # Как функция работает с отрицательными числами?
  def test_negative_numbers(self):
    self.assertEqual(two_sum([6,-1],5), [0,1])
    
  # Если не получается составить target из двух чисел списка
  def test_no_result(self):
    self.assertEqual(two_sum([1,2], 300), 'Не найдены требуемые комбинации чисел в списке')
    
  # Если есть множество ответов
  def test_multiply_answers(self):
    self.assertEqual(two_sum([1,2,3,2,1], 5), [1,2])
    
  
  
if __name__ == '__main__':
  unittest.main()

















