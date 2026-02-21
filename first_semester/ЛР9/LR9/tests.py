import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController

class TestCurrencyController(unittest.TestCase):

    def test_list_currencies(self):
        mock_db = MagicMock()
        mock_db.read.return_value = [
            {"id": 1, "char_code": "USD", "value": 90}
        ]

        controller = CurrencyController(mock_db)
        result = controller.list_currencies()

        self.assertEqual(result[0]["char_code"], "USD")
        mock_db.read.assert_called_once()

    def test_update_currency(self):
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)

        controller.update_currency("USD", 100)
        mock_db.update.assert_called_once_with("USD", 100)


if __name__ == "__main__":
    unittest.main()
