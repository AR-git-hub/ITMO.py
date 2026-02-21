
class User():
    # === Constructor ===
    def __init__(self, id, name, email):
        self.__id: int = id
        self.__name: str = name
        self.__email: str = email
        
        
        
    # === Getters/Setters ===
    ## ID
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id: int):
        if type(id) is int and id > 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании ID пользователя')
        
    ## NAME
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
          raise ValueError('Ошибка при задании имени пользователя')
    
    ## E-MAIL
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email: str):
        if type(email) is str and '@' in email and '.' in email:
            self.__email = email
        else:
            raise ValueError('Ошибка при задании электронной почты пользователя')
    
    
    
'''
# Проверка

user = User(1234, 'Петя', 'petya@gmail.com')

gets = [user.id, user.name, user.email]


for i in gets:
    print(i)
        



user.id = 12345 
user.name = 'Petya' 
user.email = 'petya_cool@rambler.ru'

gets = [user.id, user.name, user.email]

print('\n=====\n')
for i in gets:
    print(i)
    
'''