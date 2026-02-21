from http.server import BaseHTTPRequestHandler
from render import render_template
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from models import Author, User
from models.user_subscription import UserSubscription
from models import users  # <-- твоё users.py
import json
from models.currency_api import get_currencies


me_author = Author(name='AR (Aleksandr)', group='P3124')

# локальная БД только для ПОДПИСОК
users_db = {}

user_subscriptions = {}

currency_rates = {
    'USD': {'name': 'Доллар США', 'rate': 73.45, 'nominal': 74, 'date': '2024-11-15'},
    'EUR': {'name': 'Евро', 'rate': 85.67, 'nominal': 83, 'date': '2025-11-15'},
    'GBP': {'name': 'Фунт стерлингов', 'rate': 95.23, 'nominal': 120, 'date': '2025-11-15'},
    'JPY': {'name': 'Японская иена', 'rate': 0.65, 'nominal': 65, 'date': '2025-11-15'}
}

def update_all_currencies_from_api():
    try:
        rates = get_currencies()  # без аргументов
        for c, r in rates.items():
            if c in currency_rates:
                currency_rates[c]['rate'] = r
                currency_rates[c]['date'] = datetime.now().strftime("%Y-%m-%d")
            else:
                currency_rates[c] = {'name': c, 'rate': r, 'nominal': 1, 'date': datetime.now().strftime("%Y-%m-%d")}


    except Exception as e:
        print("GLOBAL UPDATE ERROR:", e)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    routes = {
        '/': 'index.html',
        '/author': 'author.html',
        '/users': 'users.html',
        '/user': 'user.html',
        '/currencies': 'currencies.html',
    }

    # ==========================
    #         GET
    # ==========================
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        template_name = self.routes.get(path)
        if not template_name:
            self.send_error(404)
            return

        # --- USERS PAGE ---
        if path == '/users':

            # ---------- CREATE ----------
            if qs.get("action", [''])[0] == 'create':
                name = qs.get('name', [''])[0]
                email = qs.get('email', [''])[0]
                if not name or not email:
                    self.send_error(400, "name and email required")
                    return
                user = users.add(name, email)
                users_db[str(user.id)] = user
                user_subscriptions[str(user.id)] = []
                self.redirect(f"/users?user={user.id}")
                return

            # ---------- UPDATE ----------
            if qs.get("action", [''])[0] == 'update':
                user_id = qs.get("user", [''])[0]
                if not users.get_by_id(user_id):
                    self.send_error(404, "User not found")
                    return
                name = qs.get("name", [''])[0]
                email = qs.get("email", [''])[0]
                users.update(user_id, name, email)

                users_db[str(user_id)] = users.get_by_id(user_id)
                self.redirect(f"/users?user={user_id}")
                return

            # ---------- DELETE ----------
            if qs.get("action", [''])[0] == 'delete':
                user_id = qs.get("user", [''])[0]
                users.delete(user_id)
                users_db.pop(str(user_id), None)
                user_subscriptions.pop(str(user_id), None)
                self.redirect("/users")
                return

            # ---------- OPERATIONS: add/delete subscription ----------
            if "user" in qs and any(k in qs for k in ('add', 'delete', 'auto_update')):
                self.handle_user_operations(qs)
                return

            # ---------- OPEN USER PAGE ----------
            if "user" in qs:
                return self.show_user_page(qs["user"][0])

            # ---------- USERS LIST ----------
            return self.show_users_list()

        # ---------- CURRENCIES ----------
        if path == '/currencies':
            try:
                response = get_currencies()
            except Exception as e:
                print("API ERROR:", e)
                response = {}

            for code, rate in response.items():
                currency_rates[code] = {
                    "name": code,
                    "rate": rate,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }

        ctx = self.decide_context('/currencies', qs)
        html = render_template("currencies.html", **ctx)
        self.respond_html(html)  # убрать return!
        return  # просто выйти из метода


       

    # ====================================================================
    #                           HELPERS
    # ====================================================================
    def respond_html(self, html, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def redirect(self, url):
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()

    # ====================================================================
    #                      USERS LIST PAGE
    # ====================================================================
    def show_users_list(self):
        users_list = []
        for u in users.get_all():
            uid = str(u.id)
            subs = user_subscriptions.get(uid, [])
            users_list.append({
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'subscription_count': len(subs)
            })
            users_db[uid] = u  # keep cache updated

        ctx = {
            'app_name': "Пользователи",
            'navigation': self.get_navigation("/users"),
            'users': users_list
        }
        html = render_template("users.html", **ctx)
        self.respond_html(html)

    # ====================================================================
    #                     USER PAGE WITH SUBSCRIPTIONS
    # ====================================================================
    def show_user_page(self, user_id):
        user = users.get_by_id(user_id)
        if not user:
            self.send_error(404, "User not found")
            return

        users_db[str(user_id)] = user  # sync

        subs = user_subscriptions.get(str(user_id), [])
        subscription_data = []
        for s in subs:
            info = currency_rates.get(s.currency_code, {})
            # Добавляем историю, если она есть; иначе создаём пустой список
            history = getattr(s, 'history', [])
            subscription_data.append({
                'code': s.currency_code,
                'name': info.get('name', s.currency_code),
                'rate': info.get('rate', 0),
                'date_added': s.date_added,
                'last_updated': info.get('date', 'N/A'),
                'history': history
            })
        # ---- данные для графика динамики (пример 90 дней назад) ----
        from datetime import timedelta

        graph_data = {}
        today = datetime.now()
        for s in subs:
            data_points = []
            for i in range(90, -1, -1):  # 90 дней назад
                date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                rate = round(currency_rates[s.currency_code]["rate"] * (1 + (i % 5 - 2)/100), 4)
                data_points.append({"date": date, "rate": rate})
            graph_data[s.currency_code] = data_points



        ctx = {
            'app_name': f"Пользователь: {user.name}",
            'navigation': self.get_navigation("/users"),
            'user': {'id': user.id, 'name': user.name, 'email': user.email},
            'subscriptions': subscription_data,
            'available_currencies': [
                {'code': c, 'name': info['name']}
                for c, info in currency_rates.items()
            ],
            'graph_data': graph_data  # <--- ДОБАВЛЕНО
        }


        html = render_template("user.html", **ctx)
        self.respond_html(html)

    # ====================================================================
    #                     SUBSCRIPTION OPERATIONS
    # ====================================================================
    def handle_user_operations(self, qs):
        uid = qs.get("user", [''])[0]
        add = qs.get("add", [''])[0]
        delete = qs.get("delete", [''])[0]
        auto_upd = qs.get("auto_update", [''])[0]

        # создать запись если нет
        if uid not in user_subscriptions:
            user_subscriptions[uid] = []

        # ---- AUTO UPDATE через API ----
        # ---- AUTO UPDATE через API ----
        if auto_upd:
            subs = user_subscriptions.get(uid, [])
            codes = [s.currency_code for s in subs]

            if codes:
                try:
                    # получаем актуальные курсы через API
                    rates = get_currencies(codes)

                    # обновляем подписки и локальные курсы
                    for s in subs:
                        s.rate = rates[s.currency_code]
                        s.touch()

                        currency_rates[s.currency_code]["rate"] = rates[s.currency_code]
                        currency_rates[s.currency_code]["date"] = datetime.now().strftime('%Y-%m-%d')

                except Exception as e:
                    print("AUTO UPDATE ERROR:", e)

            return self.redirect(f"/users?user={uid}")
        # -----------------------------------


        # ADD subscription
        if add:
            add = add.upper()

            # protect from non-existing currencies
            if add not in currency_rates:
                # если валюты нет — создаём структуру
                currency_rates[add] = {"name": add, "rate": 0, "date": "N/A"}

            if all(s.currency_code != add for s in user_subscriptions[uid]):
                user_subscriptions[uid].append(
                    UserSubscription(uid, add, datetime.now().strftime("%Y-%m-%d"))
                )

            return self.redirect(f"/users?user={uid}")

        # DELETE subscription
        if delete:
            delete = delete.upper()
            user_subscriptions[uid] = [
                s for s in user_subscriptions[uid]
                if s.currency_code != delete
            ]
            return self.redirect(f"/users?user={uid}")

    # ====================================================================
    #                   CONTEXT FOR SIMPLE PAGES
    # ====================================================================
    def decide_context(self, path, qs=None):
        qs = qs or {}

        if path == '/':
            return {
                'app_name': "Получение курса валют",
                'navigation': self.get_navigation("/"),
                'total_users': len(users.get_all()),
                'total_currencies': len(currency_rates)
            }

        if path == '/author':
            return {
                'app_name': "Об авторе",
                'navigation': self.get_navigation("/author"),
                'author_name': me_author.name,
                'author_group': me_author.group,
            }

        if path == '/currencies':
            return {
                'app_name': "Актуальный курс валют",
                'navigation': self.get_navigation("/currencies"),
                'date': datetime.now().strftime("%Y-%m-%d"),
                'currencies': [
                    {'code': c, 'name': info['name'], 'rate': info['rate'], 'date': info['date']}
                    for c, info in currency_rates.items()
                ]
            }

        return {
            'app_name': "Страница",
            'navigation': self.get_navigation("/")
        }

    # ====================================================================
    #                     NAVIGATION BAR
    # ====================================================================
    def get_navigation(self, current):
        nav = [
            {'caption': 'Основная страница', 'href': '/', 'current': current == '/'},
            {'caption': 'Об авторе', 'href': '/author', 'current': current == '/author'},
            {'caption': 'Актуальный курс валют', 'href': '/currencies', 'current': current == '/currencies'},
            {'caption': 'Список пользователей', 'href': '/users', 'current': current == '/users'}
        ]
        return nav
