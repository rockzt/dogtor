from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Importing managers.py
from .managers import ModUserManager

# Create your models here.
# Creating a moderator user
class ModUser(AbstractBaseUser, PermissionsMixin):
    """Custom Moderator User."""

    # Overwriting model user property
    # Extend (new fields)

    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=200, unique=True)
    start_date = models.DateTimeField(auto_now_add=True)
    about = models.TextField(max_length=500)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    # Model's manager - Using the manager from managers.py
    objects = ModUserManager()

    # identifier user field
    USERNAME_FIELD = "email"

    # Required fields when we run the createsuperuser command
    REQUIRED_FIELDS = ["user_name", "first_name"]

    # String method
    def __str__(self):
        return f"{self.user_name} {self.email} "