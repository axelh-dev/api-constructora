from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()

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
