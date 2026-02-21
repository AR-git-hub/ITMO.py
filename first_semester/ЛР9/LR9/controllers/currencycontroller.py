# controllers/currencycontroller.py

class CurrencyController:
    def __init__(self, db_controller):
        # db_controller — это наш CurrencyRatesCRUD из databasecontroller.py
        self.db = db_controller

    def list_currencies(self):
        # READ
        return self.db.read()

    def create_currency(self, num_code: str, char_code: str, name: str, value: float, nominal: int):
        # CREATE
        self.db.create(
            num_code=num_code,
            char_code=char_code,
            name=name,
            value=value,
            nominal=nominal
        )

    def update_currency(self, char_code, value):
        if value < 0:
            raise ValueError("Курс не может быть отрицательным")
        self.db.update(char_code, value)


    def delete_currency(self, currency_id: int):
        # DELETE
        self.db.delete(currency_id)
