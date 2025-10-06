from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)


USERNAME_FIELD = "email"
REQUIRED_FIELDS = ["username", "first_name", "last_name"]


# objects = MyAccountManager() replaces the default manager (objects = models.Manager())
# so that your custom user model (which uses email for login) knows how to
# create, validate, and manage users and superusers correctly.
objects = MyAccountManager()

# This sets the default manager for the CustomUser model to MyAccountManager.
# This allows you to use the create_user and create_superuser methods
# to create new user instances.

def __str__(self):
    return self.email


# If self.is_admin is True,
# the user will automatically be considered to have all permissions
# (view, add, edit, delete, etc.) across the system.
def has_perm(self, perm, obj=None):
    return self.is_admin


# This always returns True, meaning the user can view any app in the admin dashboard.
def has_module_perms(self, app_label):
    return True
