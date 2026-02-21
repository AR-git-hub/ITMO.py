from models.user import User

# Локальное хранилище пользователей
_users = [
    User(1, "Иван", "ivan@mail.com"),
    User(2, "Мария", "maria@mail.com"),
    User(3, "Петр", "petr@mail.com"),
]

def get_all():
    """Вернуть список всех пользователей"""
    return _users

def get_by_id(user_id: int | str):
    """Вернуть пользователя по ID или None"""
    user_id = str(user_id)
    for u in _users:
        if str(u.id) == user_id:
            return u
    return None

def add(name: str, email: str):
    """Добавить пользователя. ID генерируется автоматически."""
    if _users:
        new_id = int(_users[-1].id) + 1
    else:
        new_id = 1
    user = User(new_id, name, email)
    _users.append(user)
    return user

def update(user_id, name=None, email=None):
    """Обновить данные пользователя."""
    user = get_by_id(user_id)
    if not user:
        return False
    if name:
        user.name = name
    if email:
        user.email = email
    return True

def delete(user_id):
    """Удалить пользователя по ID."""
    global _users
    user = get_by_id(user_id)
    if not user:
        return False
    _users = [u for u in _users if str(u.id) != str(user_id)]
    return True
