from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UploadData
admin.site.register(UploadData)

# Register your models here.
