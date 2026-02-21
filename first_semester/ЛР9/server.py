from http.server import BaseHTTPRequestHandler
from render import render_template

from models import Author
from models import User

me_author = Author(name='AR (Aleksandr)', group='P3124')

some_user_1 = User(id='12321', name='Michael', email='michael@gmail.com')
some_user_2 = User(id='789987', name='Scott', email='scott@yahoo.com')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    routes = {
        '/': 'index.html',
        '/author': 'author.html',
        '/users': 'users.html',
        '/user': 'user.html',
        '/currencies': 'currencies.html',
    }

    def do_GET(self):
        path = self.path
        template_name = self.routes.get(path) # type: ignore

        if not template_name:
            self.send_error(404)
            return

        context = decide_context(path)
        html = render_template(template_name, **context)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


def decide_context(path):
    
    if path == '/': # корень (root url)
        context = {
            'app_name': "Получение курса валют",
            'navigation': [
                {'caption': 'Текущая страница', 'href': "/"},
                {'caption': 'Об авторе', 'href': '/author'},
                {'caption': 'Актуальный курс валют', 'href': '/currencies'},
                {'caption': 'О пользователях', 'href': '/users'},
                
            ]
        }
        
    if path == '/author':
        context = {
            'app_name': "Об авторе",
            'navigation': [
                {'caption': 'Основная страница', 'href': "/"},
                {'caption': 'Текущая страница', 'href': '/author'},
                {'caption': 'Актуальный курс валют', 'href': '/currencies'},
                {'caption': 'О пользователях', 'href': '/users'}
            ],
            'author_name': me_author.name,
            'author_group': me_author.group,
        }
        
    if path == '/users':
        context = {
            'app_name': "Пользователи",
            'navigation': [
                {'caption': 'Основная страница', 'href': "/"},
                {'caption': 'Об авторе', 'href': '/author'},
                {'caption': 'Актуальный курс валют', 'href': '/currencies'},
                {'caption': 'Текущая страница', 'href': '/users'}
            ],
            
            'users': [
                {'user_id': some_user_1.id, 'user_name': some_user_1.name, 'user_email': some_user_1.email},
                {'user_id': some_user_2.id, 'user_name': some_user_2.name, 'user_email': some_user_2.email}
                
            
            ]
        }
        
    if path == '/user':
        context = {
            'app_name': "Пользователь *имя*",
            'navigation': [
                {'caption': 'Основная страница', 'href': "/"},
                {'caption': 'Об авторе', 'href': '/author'},
                {'caption': 'Актуальный курс валют', 'href': '/currencies'},
                {'caption': 'Текущая страница', 'href': '#'}
            ]
        }
        
    if path == '/currencies':
        context = {
            'app_name': "Актуальный курс валют",
            'navigation': [
                {'caption': 'Основная страница', 'href': "/"},
                {'caption': 'Об авторе', 'href': '/author'},
                {'caption': 'Текущая страница', 'href': '/currencies'},
                {'caption': 'О пользователях', 'href': '/users'}
            ]
        }
        
    return context # type: ignore
            
    