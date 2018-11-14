from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin
from django.core.validators import MinValueValidator

class CustomUser(AbstractUser):
    # add additional fields in here
    uploads = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    
    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.uploads;  


    def incUploads(self):
        self.uploads += 1

    def getUploads(self):
        return self.uploads

    

