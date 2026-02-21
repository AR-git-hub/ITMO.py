from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from render import render_template

from controllers import CurrencyController
from models import Author, users
from models.user_subscription import UserSubscription
from models.currency_api import get_currencies, get_currency_history

from datetime import datetime, timedelta


# Автор
me_author = Author(name="Александр Рябков", group="P3124")

# Хранилище подписок (in-memory, как в ЛР8)
user_subscriptions: dict[str, list[UserSubscription]] = {}      # user_id → [UserSubscription]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # сюда myapp.py положит экземпляр CurrencyController
    currency_controller: CurrencyController = None

    routes = {
        '/': 'index.html',
        '/author': 'author.html',
        '/users': 'users.html',
        '/user': 'user.html',
        '/currencies': 'currencies.html',
        # CRUD валют — без шаблонов
        '/currency/create': None,
        '/currency/update': None,
        '/currency/delete': None,
    }

    # =========================================================
    #                         GET
    # =========================================================
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # Разрешаем CRUD-маршруты /currency/ без шаблона
        if path not in self.routes and not path.startswith("/currency/"):
            return self.send_error(404)

        # ---------------- ГЛАВНАЯ ----------------
        if path == '/':
            ctx = {
                'app_name': "Главная",
                'myapp': "ЛР9: MVC + SQLite + подписки",
                'navigation': self.get_navigation("/"),
                'total_users': len(users.get_all()),
                'total_currencies': len(self.currency_controller.list_currencies()),
            }
            return self.respond_html(render_template("index.html", **ctx))

        # ---------------- ОБ АВТОРЕ ----------------
        if path == '/author':
            ctx = {
                'app_name': "Об авторе",
                'navigation': self.get_navigation("/author"),
                'author_name': me_author.name,
                'author_group': me_author.group,
            }
            return self.respond_html(render_template("author.html", **ctx))

        # ======================================================
        #                         USERS
        # ======================================================
        if path == "/users":
            action = qs.get("action", [""])[0]
            user_id = qs.get("user", [""])[0] if "user" in qs else None

            # ---------- CREATE USER ----------
            if action == "create":
                name = qs.get("name", [""])[0]
                email = qs.get("email", [""])[0]

                if name and email:
                    new_user = users.add(name, email)
                    user_subscriptions[str(new_user.id)] = []

                return self.redirect("/users")

            # ---------- UPDATE USER ----------
            if action == "update":
                user_id = qs.get("user", [""])[0]
                name = qs.get("name", [""])[0]
                email = qs.get("email", [""])[0]

                user_obj = users.get_by_id(user_id)
                if not user_obj:
                    return self.send_error(404, "User not found")

                # если поле пустое — оставляем старое значение
                if not name.strip():
                    name = user_obj.name
                if not email.strip():
                    email = user_obj.email

                users.update(user_id, name, email)
                return self.redirect(f"/users?user={user_id}")

            # ---------- DELETE USER ----------
            if action == "delete":
                if user_id:
                    users.delete(user_id)
                    user_subscriptions.pop(str(user_id), None)
                return self.redirect("/users")

            # ---------- ADD / DELETE SUBSCRIPTION ----------
            if user_id and ("add" in qs or "delete" in qs):
                subs = user_subscriptions.setdefault(str(user_id), [])

                # ADD ?user=1&add=USD
                if "add" in qs:
                    code = qs["add"][0].upper()

                    if all(s.currency_code != code for s in subs):
                        # берём реальный курс (или 0, если не получилось)
                        try:
                            rate = get_currencies()[code]
                        except Exception:
                            rate = 0

                        sub = UserSubscription(
                            user_id=user_id,
                            currency_code=code,
                            date_added=datetime.now().strftime("%Y-%m-%d")
                        )
                        sub.rate = rate
                        sub.add_history(rate)
                        subs.append(sub)

                # DELETE ?user=1&delete=USD
                if "delete" in qs:
                    code = qs["delete"][0].upper()
                    user_subscriptions[str(user_id)] = [
                        s for s in subs if s.currency_code != code
                    ]

                return self.redirect(f"/users?user={user_id}")

            # ---------- USER PAGE ----------
            if user_id:
                return self.show_user_page(user_id)

            # ---------- USERS LIST ----------
            return self.show_users_list()

        # --------------- /user?id=... ---------------
        if path == "/user":
            if "id" in qs:
                return self.show_user_page(qs["id"][0])
            return self.redirect("/users")

        # ======================================================
        #                        CURRENCIES
        # ======================================================

        if path == "/currencies":
            currencies = self.currency_controller.list_currencies()
            ctx = {
                'app_name': "Валюты",
                'navigation': self.get_navigation("/currencies"),
                'currencies': currencies
            }
            return self.respond_html(render_template("currencies.html", **ctx))

        # ---------- CREATE CURRENCY ----------
        if path == "/currency/create":
            num_code = qs.get("num_code", [""])[0]
            char_code = qs.get("char_code", [""])[0]
            name = qs.get("name", [""])[0]
            value = qs.get("value", [""])[0]
            nominal = qs.get("nominal", [""])[0]

            if num_code and char_code and name and value and nominal:
                try:
                    self.currency_controller.create_currency(
                        num_code=num_code,
                        char_code=char_code.upper(),
                        name=name,
                        value=float(value),
                        nominal=int(nominal)
                    )
                except Exception as e:
                    print("CREATE ERROR:", e)

            return self.redirect("/currencies")

        # ---------- DELETE CURRENCY ----------
        if path == "/currency/delete":
            currency_id = qs.get("id", [""])[0]
            try:
                self.currency_controller.delete_currency(int(currency_id))
            except Exception as e:
                print("DELETE ERROR:", e)
            return self.redirect("/currencies")

        # ---------- UPDATE CURRENCY ----------
        if path == "/currency/update":
            # Вариант: ?char_code=USD&value=92.5
            if "char_code" in qs and "value" in qs:
                try:
                    self.currency_controller.update_currency(
                        qs["char_code"][0].upper(),
                        float(qs["value"][0])
                    )
                except Exception as e:
                    print("UPDATE ERROR:", e)
            else:
                # Вариант: ?USD=92.5
                for code, val in qs.items():
                    try:
                        self.currency_controller.update_currency(code.upper(), float(val[0]))
                    except Exception as e:
                        print("UPDATE LOOP ERROR:", e)

            return self.redirect("/currencies")

    # =========================================================
    #                        HELPERS (USERS)
    # =========================================================

    def show_users_list(self):
        ctx = {
            'app_name': "Пользователи",
            'navigation': self.get_navigation("/users"),
            'users': users.get_all()
        }
        return self.respond_html(render_template("users.html", **ctx))

    def show_user_page(self, user_id):
        user_obj = users.get_by_id(user_id)
        if not user_obj:
            return self.send_error(404, "User not found")

        subs = user_subscriptions.setdefault(str(user_id), [])

        # валюты из SQLite
        all_rates = self.currency_controller.list_currencies()

        # если в БД пусто — подкинем 3 дефолтные, чтобы можно было что-то выбрать
        if not all_rates:
            all_rates = [
                {"char_code": "USD", "name": "Доллар США"},
                {"char_code": "EUR", "name": "Евро"},
                {"char_code": "CNY", "name": "Юань"},
            ]

        today = datetime.now()
        date_to = today.strftime("%d/%m/%Y")
        date_from = (today - timedelta(days=90)).strftime("%d/%m/%Y")

        subscription_data = []
        graph_data = {}

        for sub in subs:
            code = sub.currency_code

            # история курса за 90 дней
            try:
                history = get_currency_history(code, date_from, date_to)
            except Exception:
                history = []

            if not history:
                history = [
                    {"date": (today - timedelta(days=i)).strftime("%Y-%m-%d"), "rate": None}
                    for i in range(90)
                ]

            graph_data[code] = history
            current_rate = history[-1]["rate"]

            # изменение в процентах
            percent_change = None
            if len(history) >= 2 and history[-2]["rate"] is not None and current_rate is not None:
                prev = history[-2]["rate"]
                if prev:
                    percent_change = round((current_rate - prev) / prev * 100, 2)

            cinfo = next((c for c in all_rates if c["char_code"] == code), None)
            cname = cinfo["name"] if cinfo else code

            subscription_data.append({
                "code": code,
                "name": cname,
                "rate": current_rate,
                "date_added": sub.date_added,
                "last_updated": history[-1]["date"],
                "change": percent_change
            })

        ctx = {
            'app_name': "Профиль пользователя",
            'navigation': self.get_navigation("/users"),
            'user': user_obj,
            'subscriptions': subscription_data,
            'available_currencies': [{"code": r["char_code"], "name": r["name"]} for r in all_rates],
            'graph_data': graph_data
        }

        return self.respond_html(render_template("user.html", **ctx))

    # =========================================================
    #                        GENERAL HELPERS
    # =========================================================

    def respond_html(self, html, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def get_navigation(self, current):
        return [
            {'caption': 'Главная', 'href': '/', 'current': current == '/'},
            {'caption': 'Об авторе', 'href': '/author', 'current': current == '/author'},
            {'caption': 'Валюты', 'href': '/currencies', 'current': current == '/currencies'},
            {'caption': 'Пользователи', 'href': '/users', 'current': current == '/users'},
        ]
