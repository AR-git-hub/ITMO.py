import unittest
from models.user import User
from models.currency import Currency
from models.user_currency import UserCurrency
from models.currency_api import get_currencies

class TestModels(unittest.TestCase):

    def test_user_creation(self):
        u = User(id=1, name="Test")
        self.assertEqual(u.name, "Test")
        self.assertEqual(u.id, 1)

    def test_currency_creation(self):
        c = Currency(id=1, char_code="USD", name="Dollar", value=73.5, nominal=1)
        self.assertEqual(c.char_code, "USD")
        self.assertEqual(c.value, 73.5)

    def test_user_currency(self):
        u = User(id=1, name="Test")
        c = Currency(id=1, char_code="USD", name="Dollar", value=73.5, nominal=1)
        uc = UserCurrency(id=1, user_id=u.id, currency_id=c.id)
        self.assertEqual(uc.user_id, 1)
        self.assertEqual(uc.currency_id, 1)

    def test_get_currencies(self):
        rates = get_currencies()
        self.assertIn("USD", rates)
        self.assertIsInstance(rates["USD"], float)

if __name__ == "__main__":
    unittest.main()


import unittest
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from server import SimpleHTTPRequestHandler

class DummyRequest:
    def makefile(self, *args, **kwargs):
        from io import BytesIO
        return BytesIO()

class TestServer(unittest.TestCase):

    def test_routes_exist(self):
        handler = SimpleHTTPRequestHandler(DummyRequest(), ("127.0.0.1", 0), None)
        self.assertIn("/", handler.routes)
        self.assertIn("/users", handler.routes)
        self.assertIn("/currencies", handler.routes)
        self.assertIn("/author", handler.routes)

if __name__ == "__main__":
    unittest.main()
