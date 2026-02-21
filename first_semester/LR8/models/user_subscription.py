class UserSubscription:
    def __init__(self, user_id: str, currency_code: str, date_added: str):
        self.__user_id = user_id
        self.__currency_code = currency_code
        self.__date_added = date_added
        self.rate = 0
        self.history = [] 
    @property
    def user_id(self) -> str:
        return self.__user_id
    
    @property
    def currency_code(self) -> str:
        return self.__currency_code
    
    @property
    def date_added(self) -> str:
        return self.__date_added
    
    def touch(self):
        today = datetime.now().strftime('%Y-%m-%d')
        self.history.append({'date': today, 'rate': self.rate})
