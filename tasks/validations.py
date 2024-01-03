from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()

def custom_validation(data):
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not password or len(password) < 8:
        raise ValidationError('Elige otra contraseña, mínimo 8 caracteres.')

    if not username:
        raise ValidationError('Elige otro nombre de usuario.')

    return data


def validate_username(data):
    username = data.get('username', '').strip()
    if not username:
        raise ValidationError('Elige otro nombre de usuario.')
    return True

def validate_password(data):
    password = data.get('password', '').strip()
    if not password:
        raise ValidationError('Se necesita una contraseña.')
    return True
