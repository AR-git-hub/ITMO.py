import sqlite3
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
from controllers.databasecontroller import CurrencyRatesCRUD
from controllers.currencycontroller import CurrencyController

if __name__ == "__main__":

    # === ВАЖНО ===
    # Теперь БД сохраняется в файл — данные НЕ пропадают после перезапуска.
    conn = sqlite3.connect("database.db", check_same_thread=False)

    db = CurrencyRatesCRUD(conn)
    controller = CurrencyController(db)

    # передаём контроллер в сервер
    SimpleHTTPRequestHandler.currency_controller = controller

    server = HTTPServer(("localhost", 8080), SimpleHTTPRequestHandler)
    print("Запущено на http://localhost:8080")
    server.serve_forever()
