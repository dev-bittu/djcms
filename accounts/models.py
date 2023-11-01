from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .managers import UserManager

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = (email,)

    objects = UserManager()

    def __str__(self):
        return f'User({self.id}, {self.username})'

    @staticmethod
    def password_is_valid(passwd):
        if len(passwd) < 6:
            return False
        return True

    @staticmethod
    def email_is_valid(email):
        try:
            validate = EmailValidator()
            validate(email)
            return True
        except ValidationError:
            return False
