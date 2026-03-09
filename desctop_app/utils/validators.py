# Валидаторы
# Проверка введенного логина/пароля
# Проверка введенного тега игрока


def validate_login(login: str) -> tuple[bool, str]:
    if not login:
        return False, "Логин не может быть пустым"
    if len(login) < 3:
        return False, "Логин должен содержать минимум 3 символа"
    # можно добавить проверку на допустимые символы
    return True, ""

def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 6:
        return False, "Пароль должен быть не короче 6 символов"
    return True, ""

def validate_player_tag(tag: str) -> tuple[bool, str]:
    if not tag:
        return False, "Тег не может быть пустым"

    if tag[0] != '#':
        return False, "Тег должен начинаться с символа '#'"

    if len(tag) < 5:
        return False, "После '#' должен быть хотя бы один символ"

    other_part = tag[1:]
    if not (5 <= len(other_part) <= 10):
        return False, "Основная часть тега должна содержать от 5 до 10 символов"

    for char in other_part:
        if not (char.isdigit() or ('A' <= char <= 'Z')):
            return False, "Тег может содержать только цифры и заглавные буквы (A–Z)"

    return True, ""