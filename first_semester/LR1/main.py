nums = [1, 6, -1]
target = 300


def two_sum(nums, target):
  
  # Проверяем является ли список значением класса NoneType
  if nums == None:
    return 'Список является значением класса NoneType'
  
  # Проверяем, что список является списком, а его значения - целые числа
  if type(nums) == list:
    if not all(type(x)==int for x in nums):
      return 'В списке присутсвуют не целые числовые значения'
  else:
    return 'На вход подан не список'
  
  # Проверяем, что список не пустой
  if nums == []:
    return 'На вход подан пустой список'
  
  # Проверяем, является ли target None
  if target == None:
    return 'Переменна target является значением класса NoneType'
  
  # Проверяем, является ли target целым числом
  if type(target) != int:
    return 'Переменна target не является целым числовым значением'
  
  
  
  # Сама функция
  for i in range(len(nums)):
      for j in range(i+1, len(nums)):
          if (nums[i]+nums[j]) == target:
            return [i,j] # возвращаем самые первые найденные индексы
  
  # Если не получается составить target
  return 'Не найдены требуемые комбинации чисел в списке'
          
print(two_sum(nums, target))