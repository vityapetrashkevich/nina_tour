from jose import jwt
from datetime import datetime, timedelta, UTC

from .config import settings

import string
import secrets


def generate_secure_password(length: int = 16, use_special_chars: bool = False) -> str:
    """
    Генерирует криптографически надежный пароль.

    :param length: Длина пароля (минимум 8 символов).
    :param use_special_chars: Использовать ли спецсимволы (!, @, #, и т.д.).
    :return: Строка с паролем.
    """
    if length < 8:
        length = 8  # Устанавливаем минимальный порог безопасности

    # Базовый набор: буквы в разных регистрах и цифры
    alphabet = string.ascii_letters + string.digits

    if use_special_chars:
        alphabet += string.punctuation

    # Гарантируем наличие хотя бы одного символа из каждой обязательной группы
    # (Чтобы пароль не состоял из одних цифр или только букв)
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

        # Проверки на надежность
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password) if use_special_chars else True

        if has_upper and has_lower and has_digit and has_special:
            return password


def verify_password(plain_password: str, password_hash: str) -> bool:
    return settings.crypt_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    print(password)
    password_hash = settings.crypt_context.hash(password)
    return password_hash


def create_access_token(admin_id: int) -> str:
    payload = {
        "sub": str(admin_id),
        "exp": datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
