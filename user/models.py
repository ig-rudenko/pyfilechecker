from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=256, null=True)

    class Meta:
        db_table = "user"
