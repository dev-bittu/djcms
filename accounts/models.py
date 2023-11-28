from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from .managers import UserManager

class User(AbstractUser):
    is_author = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpeg")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

