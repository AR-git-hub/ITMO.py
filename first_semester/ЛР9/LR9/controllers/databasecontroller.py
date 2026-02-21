import sqlite3

class CurrencyRatesCRUD:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self._init_schema()

    def _init_schema(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_code TEXT NOT NULL,
            char_code TEXT NOT NULL,
            name TEXT NOT NULL,
            value FLOAT,
            nominal INTEGER
        )
        """)
        self.conn.commit()

    # -------------------------
    # CREATE
    # -------------------------
    def create(self, num_code, char_code, name, value, nominal):
        sql = """
        INSERT INTO currency(num_code, char_code, name, value, nominal)
        VALUES (?, ?, ?, ?, ?)
        """
        cur = self.conn.cursor()
        cur.execute(sql, (num_code, char_code, name, value, nominal))
        self.conn.commit()

    # -------------------------
    # READ
    # -------------------------
    def read(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, num_code, char_code, name, value, nominal FROM currency")
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "num_code": r[1],
                "char_code": r[2],
                "name": r[3],
                "value": r[4],
                "nominal": r[5],
            }
            for r in rows
        ]

    # тесты используют _read(), добавляем совместимость
    def _read(self):
        return self.read()

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, char_code, value):
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (value, char_code))
        self.conn.commit()

    # -------------------------
    # DELETE
    # -------------------------
    def delete(self, currency_id: int):
        sql = "DELETE FROM currency WHERE id = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (currency_id,))
        self.conn.commit()
