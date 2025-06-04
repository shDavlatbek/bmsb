from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.main.models import School


class User(AbstractUser):
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Maktab",
    )    
    
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Adminlar"