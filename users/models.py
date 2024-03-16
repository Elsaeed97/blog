from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    """
        User Model.
    """
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email