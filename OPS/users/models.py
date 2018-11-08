from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email

   # CustomUser_slug = models.SlugField(max_length=30, blank=False, verbose_name='user slug')

