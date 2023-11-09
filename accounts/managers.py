from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class UserManager(BaseUserManager):
    """
    Custom user model manager.
    """

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('Users must have an username'))
        if email := extra_fields.get("email", ""):
            extra_fields["email"] = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_author', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)

