from http.server import BaseHTTPRequestHandler
from render import render_template
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

from models import Author, User
from models.user_subscription import UserSubscription
from models import users

# валютный API
from models.currency_api import get_currencies, get_currency_history

# никаких valute_codes больше НЕ нужно
# VALUTE_CODES = {}

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
        
        # ---------- SIMPLE PAGES ----------
        if path in ('/', '/author'):
            ctx = self.decide_context(path, qs)
            html = render_template(template_name, **ctx)
            self.respond_html(html)
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

                # подписка по умолчанию
                default_code = "USD"
                sub = UserSubscription(user.id, default_code, datetime.now().strftime("%Y-%m-%d"))
                sub.add_history(currency_rates[default_code]["rate"])
                user_subscriptions[str(user.id)].append(sub)

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
            except:
                response = {}

            for code, rate in response.items():
                currency_rates[code] = {
                    "name": code,
                    "rate": rate,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }

            ctx = self.decide_context('/currencies', qs)
            html = render_template("currencies.html", **ctx)
            self.respond_html(html)
            return



       

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

        users_db[str(user_id)] = user
        subs = user_subscriptions.get(str(user_id), [])

        subscription_data = []
        today = datetime.now()
        date_to = today.strftime("%d/%m/%Y")
        date_from = (today - timedelta(days=90)).strftime("%d/%m/%Y")

        graph_data = {}

        for s in subs:
            code = s.currency_code.upper()
            current_info = currency_rates.get(code, {})
            current_rate = None     # временно


            # история за 90 дней (кэш используется автоматически)
            try:
                history = get_currency_history(code, date_from, date_to)
            except:
                history = []

            if not history:
                history = [
                    {"date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
                    "rate": current_rate}
                    for i in range(90, -1, -1)
                ]
            # текущий курс = последний из истории
            current_rate = history[-1]["rate"]

            graph_data[code] = history

            # изменение % за последние сутки
            percent_change = None
            if len(history) >= 2:
                latest = history[-1]["rate"]
                prev = history[-2]["rate"]
                if prev > 0:
                    percent_change = round((latest - prev) / prev * 100, 2)

            subscription_data.append({
                "code": code,
                "name": current_info.get("name", code),
                "rate": current_rate,
                "date_added": s.date_added,
                "last_updated": current_info.get("date", "N/A"),
                "change": percent_change
            })

        all_rates = get_currencies()

        ctx = {
            "app_name": f"Пользователь: {user.name}",
            "navigation": self.get_navigation("/users"),
            "user": {"id": user.id, "name": user.name, "email": user.email},
            "subscriptions": subscription_data,
            "available_currencies": [{"code": c, "name": c} for c in sorted(all_rates.keys())],
            "graph_data": graph_data
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
                        s.add_history(s.rate)
                        # s.touch()

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
                
                sub = UserSubscription(uid, add, datetime.now().strftime("%Y-%m-%d"))

                # записываем РЕАЛЬНЫЙ курс валюты при добавлении
                sub.add_history(currency_rates[add]["rate"])


                user_subscriptions[uid].append(sub)


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

            currencies_list = []

            # собираем 10 последних дней — почти гарантированно есть архивы
            dates = [
                (datetime.now() - timedelta(days=i)).strftime("%d/%m/%Y")
                for i in range(10)
            ]

            for code, info in currency_rates.items():

                # берём историю за последние 10 дней
                try:
                    history = get_currency_history(code, dates[-1], dates[0])
                except:
                    history = []

                percent_change = None
                if len(history) >= 2:
                    prev = history[-2]["rate"]
                    curr = history[-1]["rate"]
                    if prev > 0:
                        percent_change = round((curr - prev) / prev * 100, 2)

                currencies_list.append({
                    'code': code,
                    'name': info['name'],
                    'rate': info['rate'],
                    'date': info['date'],
                    'change': percent_change
                })

            return {
                'app_name': "Актуальный курс валют",
                'navigation': self.get_navigation("/currencies"),
                'date': datetime.now().strftime("%Y-%m-%d"),
                'currencies': currencies_list
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
