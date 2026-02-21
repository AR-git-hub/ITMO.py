
# Примеры. id - 234, code - '074', name - 'USD'
class Currency():
    
    # === Constructor ===
    def __init__(self, id: int, code: str, name: str):
        self.__id: int = id
        self.__code: int = code
        self.__name: str = name
        
    
    # === Getters/Setters ===
    
    ## ID
    @property 
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id: int):
        if type(id)==int and id > 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании ID валюты')
        
    ## ID
    @property 
    def code(self):
        return self.__code
    
    @code.setter
    def code(self, code: str):
        if type(code)==str and len(code) == 3 and int(code) > 0: # ТОЛЬКО ТРЕХЗНАЧНЫЕ ЧИСЛА
            self.__code = code
        else:
            raise ValueError('Ошибка при задании кода валюты')
        
    ## ID
    @property 
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        if type(name)==str and len(name) == 3 and name.upper() == name: # GBP, USD
            self.__name = name
        else:
            raise ValueError('Ошибка при задании названия валюты')

    

'''
# Проверка

currency = Currency(1234, '487', 'USD')

gets = [currency.id, currency.code, currency.name]

for i in gets:
    print(i)
        

currency.id = 123456789 
currency.code = '892' 
currency.name = 'AUD' 

print('\n=====\n')

gets = [currency.id, currency.code, currency.name]

for i in gets:
    print(i)
    
'''